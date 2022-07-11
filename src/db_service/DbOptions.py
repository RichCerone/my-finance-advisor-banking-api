class DbOptions:
    """
    Database options for configuring the DbService.
    """

    def __init__(self, endpoint: str, key: str, databaseId: str, containerId: str):
        """
        Parameters
        ----------
        endpoint : str
            The endpoint for the database connection.

        key : str
            The key for accessing the database.
        
        databaseId : str
            The id of the database connecting to.

        containerId : str
            The id of the container connecting to.
        """

        self.endpoint = endpoint
        self.key = key
        self.databaseId = databaseId
        self.containerId = containerId