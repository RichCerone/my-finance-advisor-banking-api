
class InvalidParameterError(Exception):
    """
    The parameter is invalid.
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