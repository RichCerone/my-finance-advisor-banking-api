from src.token_helper.TokenHelper import TokenHelper
from src.db_service.DbService import DbService

class TokenHelperInjector:
    """
    Injects a token helper service.
    """

    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int):
        """
        Creates a new TokenHelperInjector.

        Parameters
        ----------
        secret_key: str
            The secret key to sign tokens with.
        
        algorithm: str
            The algorithm to encrypt tokens with.

        access_token_expire_minutes: int
            The time in minutes for the token to expire.
        """

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expires_minutes = access_token_expire_minutes

    def __call__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int) -> TokenHelper:
        """
        Calls the TokenHelperInjector instance.

        Parameters
        ----------
        secret_key: str
            The secret key to sign tokens with.
        
        algorithm: str
            The algorithm to encrypt tokens with.

        access_token_expire_minutes: int
            The time in minutes for the token to expire.

        Returns
        -------
        TokenHelper
            The token helper instance.
        """

        return TokenHelper(secret_key, algorithm, access_token_expire_minutes)


class DbServiceInjector:
    """
    Injects a database service.
    """

    def __init__(self, db_service: DbService):
        """
        Creates a new DbServiceInjector.

        Parameters
        ----------
        db_service: DbService
            The database service to inject.
        """

        self.dbService = db_service

    def __call__(self, db_service) -> DbService:
        """
        Calls the DbServiceInjector instance.

        Parameters
        ----------
        db_service: DbService
            The database service to inject.

        Returns
        -------
        DbService
            The db service instance.
        """

        db_service.connect()
        return db_service