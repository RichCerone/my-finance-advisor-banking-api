"""
This is a helper utility for authorizing the user in the token
by seeing if they actually exists in the database.
"""

import logging as logger

from fastapi import Depends, HTTPException, Request
from src.data_models.User import User
from src.dependencies import DbServiceInjector, TokenHelperInjector
from src.token_helper.TokenHelper import TokenHelper
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

users_db = DbServiceInjector(DbService(users_db_options))
token_helper = TokenHelperInjector(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)

def authorize_access(request: Request, token_helper: TokenHelper = Depends(token_helper), users_db: DbService = Depends(users_db)) -> str:
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
        logger.info("Decoding token.")

        user_in_token = token_helper.decode_access_token(token)

        logger.info("Token decoded. User: '{0}'".format(user_in_token))
        
        user = User(user_in_token, "_") # Note: '_' is used because we need to pass a non empty string, but also don't need the password.

        logger.info("Validating user '{0}'".format(user_in_token))

        if users_db.get(user.id, user.user) is None:
            logger.warning("User '{0}' is not authorized.".format(user_in_token))
            raise HTTPException(403, "Unauthorized.")

        logger.info("User '{0}' is authorized access.".format(user_in_token))

        return user_in_token

    except Exception as e:
        logger.exception("authorize_access exception -> An error occurred processing the token: {0}".format(e))
        raise HTTPException(500, "Authorization token cannot be processed.")