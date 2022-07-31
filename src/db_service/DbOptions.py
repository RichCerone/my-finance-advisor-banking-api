class DbOptions:
    """
    Database options for configuring the DbService.
    """

    def __init__(self, endpoint: str, key: str, database_id: str, container_id: str):
        """
        Parameters
        ----------
        endpoint : str
            The endpoint for the database connection.

        key : str
            The key for accessing the database.
        
        database_id : str
            The id of the database connecting to.

        container_id : str
            The id of the container connecting to.
        """

        self.endpoint = endpoint
        self.key = key
        self.database_id = database_id
        self.container_id = container_id