import json

class Query:
    """
    Specifies how to query the database
    """

    def __init__(self, query_str: str, where_params: dict[str, any]=None, enable_cross_partition_query=True):
        """
        Parameters
        ----------
        query_str: str
            The query string to execute.

        where_params: dict[str, any]
            The parameters to insert into the query. 'None' by default.
            Example:
                whereParams = {
                    "@id": 1
                    "@name": John
                }

        enable_cross_partition_query: bool
            Should be 'True' if the container is partitioned. 'True' by default.
        
        Raises
        ------
        ValueError
            Raised if the query_str is not defined.
        """
        if query_str is None or query_str.isspace():
            raise ValueError("'query_str' must be defined.")

        self.query_str = query_str
        self.where_params = where_params
        self.enable_cross_partition_query = enable_cross_partition_query


    def build_where_params(self) -> list[dict[str, object]]:
        """
        Builds the where parameters for the database API to use.

        Returns
        -------
        list[dict[str, object]]
            The parameter objects for the database API to consume.
        """
        if self.where_params is None or len(self.where_params) == 0:
            return None
        
        param_list = list[dict[str, object]]()
        for k in self.where_params:
            param_list.append({ "name": k, "value": self.where_params[k] })

        return param_list


    def __str__(self) -> str:
        formatted_where_params = "Not defined."

        if self.where_params is not None and len(self.where_params) > 0:
            formatted_where_params = json.dumps(self.where_params)

        return "'query_str': '{0}' | 'where_params': '{1}' | 'enable_cross_partition_query': {2}".format(self.query_str, formatted_where_params, self.enable_cross_partition_query)