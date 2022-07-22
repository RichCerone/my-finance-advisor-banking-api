import json
import logging as logger

from fastapi import APIRouter, HTTPException, Depends
from decimal import Decimal
from src.db_service.DbService import DbService, DbOptions
from src.db_service.Query import Query
from src.dependencies import DbServiceInjector
from src.exceptions.InvalidParameterError import InvalidParameterError
from src.exceptions.NoResultsFoundError import NoResultsFoundError
from src.libs.api_model_mappers.account_mapper import map_to_account_api_model, map_to_account_api_models
from src.libs.api_model_mappers.api_result_mapper import map_to_api_result
from src.libs.api_models.ApiResult import ApiResult
from src.libs.utils.authorize import authorize_access
from src.authorization.JwtBearer import inject_jwt_bearer
from src.documentation.docs import *
from src.config import Settings

router = APIRouter(
    prefix="/accounts",
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
    ENDPOINT, 
    KEY,
    DATABASE_ID,
    ACCOUNTS_CONTAINER_ID
)

accounts_db = DbServiceInjector(DbService(db_options))

@router.get("/", status_code=200, responses=get_accounts_responses, response_model=ApiResult, tags=["accounts"])
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
    """
    Gets accounts based on search parameters. Searching by 'id' or 'account_name' will always return one result.
    """

    try:
        logger.debug("User {0} querying accounts by 'id': '{1}', 'account_id': '{2}', 'accountName': '{3}', 'account_type': '{4}', 'account_institution': '{5}', balance: '{6}', 'page': '{7}', 'results_per_page': '{8}'"
        .format(user, id, account_id, account_name, account_type, account_institution, balance, page, results_per_page))
        logger.debug("Validating parameters passed are valid.")

        __validate_get_accounts_param(id, account_id, account_name, account_type, account_institution, balance, page, results_per_page)

        logger.debug("Parameters are valid.")

        queried: bool = False
        results = None

        # Get by key.
        if id != "":
            results = accounts_db.get(id, id.split("::")[1])
            
        elif account_id != "":
            results = accounts_db.get("account::{0}".format(account_id), account_id)
            
        # Query.
        else:
            queried = True

            logger.debug("Building query.")

            query = __build_get_query(account_name, account_type, account_institution, balance, page, results_per_page)

            logger.debug("Query built: '{0}'".format(query.queryStr))
            logger.info("Querying accounts by 'accountName': '{0}', 'account_type': '{1}', 'account_institution': '{2}', balance: '{3}', 'page': '{4}', 'results_per_page': '{5}'"
            .format(account_name, account_type, account_institution, balance, page, results_per_page))

            results = accounts_db.query(query)

        if results != None:
            if queried:
                accounts = map_to_account_api_models(json.loads(results))
                response = map_to_api_result(accounts, accounts.__len__(), page)

                logger.info("{0} results found.".format(accounts.__len__()))

            else:
                accounts = map_to_account_api_model(json.loads(results))
                response = map_to_api_result(accounts, 1, page)

                logger.info("1 result found.")

            logger.debug("Results: {0}".format(results))

            return response

        else:
            raise NoResultsFoundError("No accounts found based on search parameters.")
    
    except Exception as e:
        logger.exception("GET exception on 'get' -> {0}".format(e))

        if e.__class__ == InvalidParameterError:
            raise HTTPException(status_code=400, detail=e.message)

        elif e.__class__ == NoResultsFoundError:
            raise HTTPException(status_code=404, detail="No results found based on search parameters given.")

        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# Validates parameters for the GET operation.
def __validate_get_accounts_param(id: str, account_id: str, account_name: str, account_type: str, account_institution: str, balance: Decimal, page: int, results_per_page: int):
        if id != "" and id.isspace():
             raise InvalidParameterError("id is invalid (did you pass only spaces?).")

        elif id != "" and (id.split("::").__len__() == 0 or id.split("::")[0] != "accounts"):
            raise InvalidParameterError("id is not a valid format. Accepted format: accounts::[account_id]. You put: '{0}').".format(id))
        
        if account_id != "" and account_id.isspace():
            raise InvalidParameterError("account_id is invalid (did you pass only spaces?).")

        if account_name != "" and account_name.isspace():
            raise InvalidParameterError("account_name is invalid (did you pass only spaces?).")

        if account_type != "" and account_type.isspace():
            raise InvalidParameterError("account_type is invalid (did you pass only spaces?).")

        if account_institution != "" and account_institution.isspace():
            raise InvalidParameterError("account_institution is invalid (did you pass only spaces?).")
        
        if balance != None and balance.as_tuple().exponent != -2:
            raise InvalidParameterError("balance must be defined as a monetary value with exactly 2 decimal places. Example: '1000.00'. You put: '{0}'".format(balance))

        if page <= 0:
            raise InvalidParameterError("page must be greater than 1.")

        if results_per_page <= 0 or results_per_page > MAX_PAGE_SIZE:
            raise InvalidParameterError("results_per_page must be between 1 to 100 inclusive.")


# Builds a search query.
def __build_get_query(account_name: str, account_type: str, account_institution: str, balance: Decimal, page: int, results_per_page: int) -> Query:
    query_str = "SELECT * FROM {0} WHERE ".format(ACCOUNTS_CONTAINER_ID)
    where_params = dict[str, any]()
    params = list()
    
    # Determine limit and offset.
    limit = results_per_page

    if page > 1:
        offset = ((page - 1) * MAX_PAGE_SIZE)
    
    else:
        offset = 0

    if account_name != "":
        account_name_param = "{0}.account_name LIKE @account_name".format(ACCOUNTS_CONTAINER_ID)
        params.append(account_name_param)

        where_params["@account_name"] = "%" + account_name + "%"

    if account_type != "":
        account_type_param = "{0}.account_type=@account_type".format(ACCOUNTS_CONTAINER_ID)
        params.append(account_type_param)

        where_params["@account_type"] = account_type

    if account_institution != "":
        account_institution_param = "{0}.account_institution=@account_institution".format(ACCOUNTS_CONTAINER_ID)
        params.append(account_institution_param)

        where_params["@account_institution"] = account_institution

    if balance != None:
        balance_param = "{0}.balance=@balance".format(ACCOUNTS_CONTAINER_ID)
        params.append(balance_param)

        where_params["@balance"] = balance.__str__()

    # Build query with gather parameters.
    for i in range(params.__len__()):
        if (i == params.__len__() - 1):
            query_str += params[i]

        else:
            query_str += "{0} AND ".format(params[i])

    query_str += " OFFSET {0} LIMIT {1}".format(offset, limit)

    print(query_str)

    return Query(query_str, where_params)

