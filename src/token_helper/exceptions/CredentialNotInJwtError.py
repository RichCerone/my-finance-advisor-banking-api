class CredentialNotInJwtError(Exception):
    """
    The credential expected in the JWT was not present.
    """

    def __init__(self, message: str = None):
        """
        Parameters
        ----------
        message: str
            Message to include in the exception.
        """

        self.message = message,
        super().__init__(self, message)