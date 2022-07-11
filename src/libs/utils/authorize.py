"""
This is a helper utility for authorizing the user in the token
by seeing if they actually exists in the database.
"""

import logging as logger

from fastapi import HTTPException, Request
from src.data_models.User import User
from src.dependencies import DbServiceInjector, TokenHelperInjector
from src.db_service.DbService import DbOptions, DbService
from src.config import Settings

settings = Settings()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ENDPOINT = settings.endpoint
KEY = settings.key
DATABASE_ID = settings.database_id
USERS_CONTAINER_ID = settings.users_container_id
ORIGIN_LIST = settings.origins.split(",")

users_db_options = DbOptions(
        settings.endpoint, 
        settings.key,
        settings.database_id,
        settings.users_container_id
    )

# This acts as the parent DB connection in memory to prevent multiple connections from being created.
_users_db = DbService(users_db_options)

users_db = DbServiceInjector(_users_db)
token_helper = TokenHelperInjector(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

def authorize_access(request: Request) -> str:
    """
    Authorizes access based on the token

    Parameters
    ----------
    request: Request
        The incoming HTTP request.

    Raises
    ------
    HttpException
        403 - if token is not authorized.
        500 - if an error occurs processing the token.

    Returns
    -------
    str
        The username in the token.
    """

    try:
        logger.info("Getting authorization token from header 'Authorization'.")
        
        token = request.headers["Authorization"].split()[1]

        logger.info("Token retrieved.")
        logger.debug("Initializing token helper service to decode token.")
        
        tk_helper = token_helper(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
        
        logger.debug("Token helper service initialized.")
        logger.info("Decoding token.")

        user_in_token = tk_helper.decode_access_token(token)

        logger.info("Token decoded. User: '{0}'".format(user_in_token))
        logger.debug("Initializing users database for user authorization.")

        db = users_db(_users_db)
        
        user = User(user_in_token, "_") # Note: '_' is used because we need to pass a non empty string, but also don't need the password.

        logger.info("Validating user '{0}'".format(user_in_token))

        if db.get(user.id, user.user) is None:
            logger.warning("User '{0}' is not authorized.".format(user_in_token))
            raise HTTPException(403, "Unauthorized.")

        logger.info("User '{0}' is authorized access.".format(user_in_token))

        return user_in_token

    except Exception as e:
        logger.exception("authorize_access exception -> An error occurred processing the token: {0}".format(e))
        raise HTTPException(500, "Authorization token cannot be processed.")