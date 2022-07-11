from decimal import Decimal
from http.client import HTTPException
import logging as logger

from fastapi import APIRouter, Depends
from src.db_service.DbService import DbService, DbOptions
from src.db_service.Query import Query
from src.dependencies import DbServiceInjector
from src.exceptions.InvalidParameterError import InvalidParameterError
from src.libs.utils.authorize import authorize_access
from src.authorization.JwtBearer import inject_jwt_bearer
from src.config import Settings

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[
        Depends(inject_jwt_bearer)
    ]
)

settings = Settings()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ENDPOINT = settings.endpoint
KEY = settings.key
DATABASE_ID = settings.database_id
ACCOUNTS_CONTAINER_ID = settings.accounts_container_id
MAX_PAGE_SIZE = settings.max_page_size
ORIGIN_LIST = settings.origins.split(",")

db_options = DbOptions(
    settings.endpoint, 
    settings.key,
    settings.database_id,
    settings.users_container_id
)

accounts_db = DbServiceInjector(DbService(db_options))

@router.get("/", status_code=200)
def get(id: str = "",
    account_id: str = "",
    account_name: str = "",
    account_type: str = "",
    account_institution: str = "",
    balance: Decimal = None,
    page: int = 1,
    results_per_page: int = 10,
    accounts_db: DbService = Depends(accounts_db), 
    user: str = Depends(authorize_access)):
    try:
        logger.debug("User {0} querying accounts by 'id': '{1}', 'account_id': '{2}', 'accountName': '{3}', 'account_type': '{4}', 'account_institution': '{5}', 'account_type': '{6}', balance: '{7}', 'page': '{8}', 'results_per_page': '{9}'"
        .format(id, account_id, account_name, account_name, account_type, account_institution, balance, page, results_per_page))
        logger.debug("Validating parameters passed are valid.")

        __validate_get_accounts_param(id, account_id, account_name, account_type, account_institution, balance, page, results_per_page)

        logger.debug("Parameters are valid.")
        logger.info("Querying accounts by 'id': '{1}', 'account_id': '{2}', 'accountName': '{3}', 'account_type': '{4}', 'account_institution': '{5}', 'account_type': '{6}', balance: '{7}', 'page': '{8}', 'results_per_page': '{9}'"
        .format(id, account_id, account_name, account_name, account_type, account_institution, balance, page, results_per_page))

        query = __build_get_query(id, account_id, account_name, account_name, account_type, account_institution, balance, page, results_per_page)

        results = accounts_db.query(query)

        if results != None:
            return results

        else:
            raise HTTPException(404, "No accounts found based on search parameters.")

    except Exception as e:
        return ""

    return ""


def __validate_get_accounts_param(id: str, account_id: str, account_name: str, account_type: str, account_institution: str, balance: Decimal, page: int, results_per_page: int):
        if id.isspace():
             raise InvalidParameterError("id is invalid (did you pass only spaces?).")
        
        if account_id.isspace():
            raise InvalidParameterError("account_id is invalid (did you pass only spaces?).")

        if account_name.isspace():
            raise InvalidParameterError("account_name is invalid (did you pass only spaces?).")

        if account_type.isspace():
            raise InvalidParameterError("account_type is invalid (did you pass only spaces?).")

        if account_institution.isspace:
            raise InvalidParameterError("account_institution is invalid (did you pass only spaces?).")
        
        if balance.as_tuple().exponent != 2:
            raise InvalidParameterError("balance must be defined as a monetary value with exactly 2 decimal places. Example: '1000.00'.")

        if page <= 0:
            raise InvalidParameterError("page must be greater than 1.")

        if results_per_page <= 0 or results_per_page > MAX_PAGE_SIZE:
            raise InvalidParameterError("results_per_page must be between 1 to 100 inclusive.")


def __build_get_query(id: str, account_id: str, account_name: str, account_type: str, account_institution: str, balance: Decimal, page: int, results_per_page: int) -> Query:
    query_str = "SELECT * FROM {0} WHERE ".format(ACCOUNTS_CONTAINER_ID)
    where_params = dict(str, any)
    limit = results_per_page

    if page > 1:
        offset = (page * MAX_PAGE_SIZE)
    
    else:
        offset = 0

    if id:
        id_param = "{0}.id=@id".format(ACCOUNTS_CONTAINER_ID)
        query_str += "{0} LIMIT {1} OFFSET {2}".format(id_param, limit, offset)
        where_params["@id"] = id

        return Query(query_str, where_params)

    if account_id:
        account_id_param = "{0}.account_id=@id".format(ACCOUNTS_CONTAINER_ID)
        query_str += "{0} LIMIT {1} OFFSET {2}".format(account_id, limit, offset)
        where_params["@account_id"] = account_id_param

        return Query(query_str, where_params)