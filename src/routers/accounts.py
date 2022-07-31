import json
import logging as logger

from fastapi import APIRouter, HTTPException, Depends
from decimal import Decimal

from requests import put
from src.db_service.DbService import DbService, DbOptions
from src.db_service.Query import Query
from src.dependencies import DbServiceInjector
from src.exceptions.InvalidParameterError import InvalidParameterError
from src.exceptions.NoResultsFoundError import NoResultsFoundError
from src.exceptions.ObjectConflictError import ObjectConflictError
from src.libs.api_model_mappers.account_mapper import map_to_account_api_model, map_to_account_api_models, map_to_account_data_model
from src.libs.api_model_mappers.api_result_mapper import map_to_api_result
from src.data_models.Account import Account
from src.libs.api_models.UpdateAccountModel import UpdateAccountModel
from src.libs.api_models.AccountModel import AccountModel
from src.libs.api_models.ApiResult import ApiResult
from src.libs.utils.authorize import authorize_access
from src.authorization.JwtBearer import inject_jwt_bearer
from src.documentation.docs import *
from src.config import Settings

# Define router.
router = APIRouter(
    prefix="/accounts",
    dependencies=[
        Depends(inject_jwt_bearer)
    ]
)

# Services setup.
# Get settings from .env.
settings = Settings()

# Assign settings to constants.
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ENDPOINT = settings.endpoint
KEY = settings.key
DATABASE_ID = settings.database_id
ACCOUNTS_CONTAINER_ID = settings.accounts_container_id
MAX_PAGE_SIZE = settings.max_page_size
ORIGIN_LIST = settings.origins.split(",")

# Setup DB settings to inject.
db_options = DbOptions(
    ENDPOINT, 
    KEY,
    DATABASE_ID,
    ACCOUNTS_CONTAINER_ID
)

# Inject db.
accounts_db = DbServiceInjector(DbService(db_options))

# End of services setup.

# Start of router program.
"""
GET Account(s)
"""
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

        queried = False
        results = None

        # Get by key.
        if id != "":
            results = accounts_db.get(id, id.split("::")[1])
            
        elif account_id != "":
            key = Account(account_id).create_id(account_id)
            results = accounts_db.get(key, account_id)
            
        # If no key defined--query.
        else:
            queried = True

            logger.debug("Building query.")

            query = __build_get_query(account_name, account_type, account_institution, balance, page, results_per_page)

            logger.debug("Query built: '{0}'".format(query.query_str))
            logger.info("Querying accounts by 'accountName': '{0}', 'account_type': '{1}', 'account_institution': '{2}', balance: '{3}', 'page': '{4}', 'results_per_page': '{5}'"
            .format(account_name, account_type, account_institution, balance, page, results_per_page))

            results = accounts_db.query(query)

        if results != None:
            if queried:
                accounts = map_to_account_api_models(json.loads(results))
                response = map_to_api_result(accounts, len(accounts), page)

                logger.info("{0} results found.".format(len(accounts)))

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

        if type(e) == InvalidParameterError:
            raise HTTPException(status_code=400, detail=e.message)

        elif type(e) == NoResultsFoundError:
            raise HTTPException(status_code=404, detail="No results found based on search parameters given.")

        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


"""
POST Account
"""
@router.post("/", status_code=201, responses=post_account_responses, response_model=ApiResult, tags=["accounts"])
def post(account: AccountModel,  accounts_db: DbService = Depends(accounts_db), user: str = Depends(authorize_access)):
    """
    Creates a new account.
    """

    try:
        logger.debug("User {0} creating account.".format(user))
        logger.debug("Validating account model.")

        __validate_account(account)

        logger.debug("Account model is valid.")
        logger.debug("Checking if account '{0}' already exists.".format(account.account_id))

        # Check if account already exists.
        account_data_model = map_to_account_data_model(account)
        if accounts_db.get(account_data_model.id, account_data_model.account_id) != None:
            raise ObjectConflictError("Account '{0}' already exists.".format(account_data_model.account_id))
        
        # Create account.
        logger.debug("Account '{0}' does not exist.".format(account_data_model.account_id))
        logger.info("Creating account.")

        accounts_db.upsert(account_data_model.__dict__)
        
        logger.info("Account '{0}' created.".format(account_data_model.account_id))
        logger.debug("User {0} created account: {1}".format(user, str(account_data_model)))

        return map_to_api_result(account_data_model, 1, 0)

    except Exception as e:
        logger.exception("POST exception on 'post' -> {0}".format(e))

        if type(e) == InvalidParameterError:
            raise HTTPException(status_code=400, detail=e.message)

        elif type(e) == ObjectConflictError:
            raise HTTPException(status_code=409, detail=e.message)

        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


"""
PUT Account
"""
@router.put("/", status_code=200, responses=put_account_responses, response_model=ApiResult, tags=["accounts"])
def put(account_to_update: UpdateAccountModel, accounts_db: DbService = Depends(accounts_db), user: str = Depends(authorize_access)):
    """
    Updates an account's name and/or balance. You must specify the account_id, but you can omit any other fields you do not want
    to update. You must specify at least one field besides the account_id.
    """
    try:
        logger.debug("User {0} updating account.".format(user))
        logger.debug("Validating account data to update.")

        __validate_update_account(account_to_update)

        logger.debug("Account update model is valid.")
        logger.debug("Getting account '{0}' to update.".format(account_to_update.account_id))
        
        key = Account(account_to_update.account_id).create_id(account_to_update.account_id)
        account_json = accounts_db.get(key, account_to_update.account_id)
        
        # Check if account exists.
        if account_json == None:
            raise NoResultsFoundError("Could not find an account with id '{0}'".format(account_to_update.account_id))

        logger.debug("Account '{0}' found".format(account_to_update.account_id))
        logger.info("Updating account.")

        # Update account.
        account : dict[str, any] = json.loads(account_json)
        if account_to_update.account_name != None:
            account["account_name"] = account_to_update.account_name

        if account_to_update.balance != None:
            account["balance"] = account_to_update.balance

        updated_account_json = accounts_db.upsert(account)

        logger.debug("User {0} updated account: {1}".format(user, updated_account_json))

        updated_account = map_to_account_api_model(account)
        result = map_to_api_result(updated_account, 1, 0)

        logger.info("Account '{0}' updated.".format(updated_account.account_id))

        return result

    except Exception as e:
        logger.exception("PUT exception on 'put' -> {0}".format(e))

        if type(e) == InvalidParameterError:
            raise HTTPException(status_code=400, detail=e.message)

        elif type(e) == NoResultsFoundError:
            raise HTTPException(status_code=404, detail=e.message)

        else:
            raise HTTPException(status_code=500, detail="An unexpected error occurred.")


"""
Private Methods
"""
# Validates parameters for the GET operation.
def __validate_get_accounts_param(id: str, account_id: str, account_name: str, account_type: str, account_institution: str, balance: Decimal, page: int, results_per_page: int):
        if id != "" and id.isspace():
             raise InvalidParameterError("id is invalid (did you pass only spaces?).")

        elif id != "" and (len(id.split("::")) == 0 or id.split("::")[0] != "account"):
            raise InvalidParameterError("id is not a valid format. Accepted format: account::[account_id]. You put: '{0}').".format(id))
        
        if account_id != "" and account_id.isspace():
            raise InvalidParameterError("account_id is invalid (did you pass only spaces?).")

        if account_name != "" and account_name.isspace():
            raise InvalidParameterError("account_name is invalid (did you pass only spaces?).")

        if account_type != "" and account_type.isspace():
            raise InvalidParameterError("account_type is invalid (did you pass only spaces?).")

        if account_institution != "" and account_institution.isspace():
            raise InvalidParameterError("account_institution is invalid (did you pass only spaces?).")
        
        __validate_balance(balance)

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

        where_params["@balance"] = str(balance)

    # Build query with gathered parameters.
    for i in range(len(params)):
        if (i == len(params) - 1):
            query_str += params[i]

        else:
            query_str += "{0} AND ".format(params[i])

    query_str += " OFFSET {0} LIMIT {1}".format(offset, limit)

    return Query(query_str, where_params)


# Validates the account is valid.
def __validate_account(account: AccountModel):
    if account == None:
        raise InvalidParameterError("The account must be defined.")

    if not account.account_id or account.account_id.isspace():
        raise InvalidParameterError("account_id must be defined.")

    if not account.account_name or account.account_name.isspace():
        raise InvalidParameterError("account_name must be defined.")

    if not account.account_type or account.account_type.isspace():
        raise InvalidParameterError("account_type must be defined.")

    if not account.account_institution or account.account_institution.isspace():
        raise InvalidParameterError("account_institution must be defined.")

    if not account.balance or account.balance.isspace():
        raise InvalidParameterError("balance must be defined.")

    __validate_balance(account.balance)


# Validates the update account model is valid.
def __validate_update_account(account: UpdateAccountModel):
    if account.account_id == None:
        raise InvalidParameterError("The account_id must be defined.")

    if account.account_name == None and account.balance == None:
        raise InvalidParameterError("You must specify a property to update: Either 'account_name' and/or 'balance'.")

    if account.account_name != None and (not account.account_name or account.account_name.isspace()):
        raise InvalidParameterError("account_name cannot be empty.")

    if account.balance != None:
        __validate_balance(account.balance)


# Validate the balance is in a decimal format and has exactly 2 decimal places.
def __validate_balance(balance: str):
    if not balance or balance.isspace():
        raise InvalidParameterError("balance must be defined.")

    if "." not in balance:
        raise InvalidParameterError("balance must be a decimal. You put '{0}'".format(balance))

    if Decimal(balance).as_tuple().exponent != -2:
        raise InvalidParameterError("balance must have 2 decimal places. You put '{0}'".format(balance))