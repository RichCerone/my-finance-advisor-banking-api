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

    def __call__(self) -> TokenHelper:
        """
        Calls the TokenHelperInjector instance.

        Returns
        -------
        TokenHelper
            The token helper instance.
        """

        return TokenHelper(self.secret_key, self.algorithm, self.access_token_expires_minutes)


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

        self.db_service = db_service

    def __call__(self) -> DbService:
        """
        Calls the DbServiceInjector instance.

        Returns
        -------
        DbService
            The db service instance.
        """

        self.db_service.connect()
        return self.db_service