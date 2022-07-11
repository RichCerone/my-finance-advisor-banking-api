import json
import logging as logger # TODO: Need a way to configure logging dynamically.
from src.db_service.DbOptions import DbOptions
from src.db_service.Query import Query

from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError

class DbService():
    """
    Manages connections or operations to the database.

    Attributes
    ----------
    dbOptions: DbOptions
            Options for configuring the database service.

    Methods
    -------
    connect()
        Connects to the database.

    get()
        Gets an item in the database collection.

    upsert()
        Upserts an item in the database collection.
    """

    def __init__(self, dbOptions: DbOptions):
        """        
        Parameters
        ----------
        dbOptions: DbOptions
            Options for configuring the database service.
        """
        self.dbOptions = dbOptions
        self.client = None
        self.db = None
        self.container = None


    def connect(self) -> None:
        """
        Connects to the database.

        Raises
        ------
        Exception
            Raised if an unexpected error occurs.
        """

        try: # Validate the dbOptions before connecting.
            logger.debug("Validating DB options.")
            
            self.__validate_db_options()

            logger.debug("DB options are valid.")

        except Exception as e:
            logger.exception("connect exception -> Error validating db options: {0}".format(e))
            raise

        try: # Open database connection.
            logger.info("Opening connection to database.")
            logger.debug("endpoint: {0}, key: {1}".format(self.dbOptions.endpoint, self.dbOptions.key))

            self.client = CosmosClient(self.dbOptions.endpoint, self.dbOptions.key)

            logger.info("Database connection opened.")

        except Exception as e:
            logger.exception("connect exception -> Error opening connection to the database: {0}".format(e))
            raise
        
        try: # Get database.
            logger.info("Getting database {0}.".format(self.dbOptions.databaseId))

            self.db = self.client.get_database_client(self.dbOptions.databaseId)

            logger.info("Database retrieved.")
        
        except Exception as e:
            logger.exception("connect exception -> Error getting database: {0}".format(e))
            raise
        
        try: # Get container.
            logger.info("Getting container {0}.".format(self.dbOptions.containerId))

            self.container = self.db.get_container_client(self.dbOptions.containerId)

            logger.info("Container retrieved.")
        
        except Exception as e:
            logger.exception("connect exception -> Error getting container: {0}".format(e))
            raise


    def get(self, id: str, partitionKey: str) -> str:
        """
        Gets an item from the database.

        Parameters
        ----------
        id: str
            The unique id of the item being retrieved.

        partitionKey: str
            The partition key used for the database item collection.

        Returns
        -------
        str
            The JSON document of the item in the collection this database is querying.

        Raises
        ------
        ValueError
            Raised if the parameters given are invalid.

        CosmosHttpResponseError
            Raised if the item could not be retrieved.

        Exception
            Raised if an unexpected error occurs.
        """

        try:
            logger.debug("Validating parameter 'id' and 'partitionKey'.")
            
            self.__validate_id_and_partition_key(id, partitionKey)
            
            logger.debug("'id' and 'partitionKey' are valid.")

        except ValueError as e:
            logger.exception("get exception -> Parameter invalid: {0}".format(e))
            raise

        try:
            logger.info("Getting item by id: {0}".format(id))
            logger.debug("id: {0}, partitionKey: {1}".format(id, partitionKey))

            response = self.container.read_item(item=id, partition_key=partitionKey)

            logger.info("Item retrieved: {0}.".format(response))
            
            # Convert result to json and return generic object.
            j = json.dumps(response)

            return j

        except CosmosHttpResponseError as e:
            logger.warning("Could not get item by id {0} with partition key {1}.".format(id, partitionKey))
            return None

        except Exception as e:
            logger.exception("get exception -> Error getting item by id: {0}".format(e))
            raise

    
    def query(self, query: Query) -> str:
        """
        Queries the database with a given search query string.

        Parameters
        ----------
        query: Query
            The query information to use for the query's execution.

        Returns
        -------
        str
            The JSON documents from the result as a JSON string.

        Raises
        ------
        Exception
            Raised if an unexpected error occurs.
        """
        try:
            logger.debug("Validating 'query' is valid.")

            if query is None:
                raise TypeError("'query' must be defined.")

            logger.debug("'query' is valid.")
        
        except TypeError as e:
            logger.exception("query exception -> Parameters are invalid: {0}".format(e))
            raise

        try:
            logger.debug("Building where params for database API.")

            params = query.build_where_params()

            logger.debug("Where params built: {0}".format(json.dumps(params)))
            logger.info("Querying database with: {0}".format(query.__str__()))

            if params is None:
                result = list(self.container.query_items(
                    query.queryStr,
                    enable_cross_partition_query=query.enableCrossPartitionQuery))

            else:
                result = list(self.container.query_items(
                    query.queryStr,
                    parameters=params,
                    enable_cross_partition_query=query.enableCrossPartitionQuery))

            if result is not None and len(result) > 0:
                j = json.dumps(result)

                logger.info("{0} results retrieved: {1}".format(len(result), j))

                return j

            else:
                logger.warning("No results found for given query: {0}".format(query.__str__()))
                return None

        except Exception as e:
            logger.exception("query exception -> Error querying items: {0}".format(e))
            raise


    def upsert(self, item: dict[str, any]) -> str:
        """
        Upserts an item in the database.

        Parameters
        ----------
        item: dict[str, any]
            The object's dictionary key value pair.

        Returns
        -------
        str
            The JSON document of the object upserted.

        Raises
        ------
        TypeError
            Raised if the parameter given is invalid.

        Exception
            Raised if an unexpected error occurs.

        """

        try:
            logger.debug("Validating parameter 'item' is valid.")

            if item is None:
                raise TypeError("The item must be defined.")

            logger.debug("Parameter 'item' is valid.")

        except TypeError as e:
            logger.exception("upsert exception -> Parameter invalid: {0}".format(e))
            raise

        try:
            logger.info("Getting item: {0}".format(json.dumps(item)))

            result = self.container.upsert_item(item)
            
            # Convert result to json and return generic object.
            j = json.dumps(result)

            logger.info("Item retrieved: {0}".format(j))

            return j
        
        except Exception as e:
            logger.exception("upsert exception -> Error upserting item: {0}".format(e))
            raise
    
    
    def delete(self, id: str, partitionKey: str) -> None:
        """
        Deletes an item from the database.

        Parameters
        ----------
         id: str
            The unique id of the item being retrieved.

        partitionKey: str
            The partition key used for the database item collection.

        Raises
        ------
        ValueError
            Raised if the parameters given are invalid.

        CosmosResourceNotFoundError
            Raised if the item cannot be found to be deleted.

        Exception
            Raised if an unexpected error occurs.
        """
        
        try:
            logger.debug("Validating parameter 'id' and 'partitionKey'.")
            
            self.__validate_id_and_partition_key(id, partitionKey)
            
            logger.debug("'id' and 'partitionKey' are valid.")

        except ValueError as e:
            logger.exception("delete exception -> Parameter invalid: {0}".format(e))
            raise

        try:
            logger.info("Deleting item by id: '{0}'".format(id))
            logger.debug("id: {0}, partitionKey: {1}".format(id, partitionKey))

            self.container.delete_item(item=id, partition_key=partitionKey)

            logger.info("Item with id '{0}' deleted.".format(id))

        except CosmosResourceNotFoundError as e:
            logger.exception("delete exception -> Could not find item to delete: {0}".format(e))
            raise
        
        except Exception as e:
            logger.exception("delete exception -> Error deleting item: {0}".format(e))
            raise


    """
    Private Methods
    """

    # Validates the db options.
    def __validate_db_options(self) -> None:
        if self.dbOptions is None:
            raise TypeError("dbOptions cannot be 'None'.")
        
        if not self.dbOptions.endpoint or self.dbOptions.endpoint.isspace():
            raise ValueError("The endpoint must be defined.")
        
        elif not self.dbOptions.key or self.dbOptions.key.isspace():
            raise ValueError("The key must be defined.")

        elif not self.dbOptions.databaseId or self.dbOptions.databaseId.isspace():
            raise ValueError("The database id must be defined.")

        elif not self.dbOptions.containerId or self.dbOptions.containerId.isspace():
            raise ValueError("The container id must be defined.")


    # Validates the id and partition key are valid.
    def __validate_id_and_partition_key(self, id: str, partitionKey: str) -> None:
        if not id or id.isspace():
            raise ValueError("id must be defined.")

        elif not partitionKey or partitionKey.isspace():
            raise ValueError("partitionKey must be defined.")
