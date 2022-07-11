import json

class Query:
    """
    Specifies how to query the database
    """

    def __init__(self, queryStr: str, whereParams: dict[str, any]=None, enableCrossPartitionQuery=True):
        """
        Parameters
        ----------
        queryStr: str
            The query string to execute.

        whereParams: dict[str, any]
            The parameters to insert into the query. 'None' by default.
            Example:
                whereParams = {
                    "@id": 1
                    "@name": John
                }

        enableCrossPartitionQuery: bool
            Should be 'True' if the container is partitioned. 'True' by default.
        
        Raises
        ------
        ValueError
            Raised if the queryStr is not defined.
        """
        if queryStr is None or queryStr.isspace():
            raise ValueError("'queryStr' must be defined.")

        self.queryStr = queryStr
        self.whereParams = whereParams
        self.enableCrossPartitionQuery = enableCrossPartitionQuery


    def build_where_params(self) -> list[dict[str, object]]:
        """
        Builds the where parameters for the database API to use.

        Returns
        -------
        list[dict[str, object]]
            The parameter objects for the database API to consume.
        """
        if self.whereParams is None or len(self.whereParams) == 0:
            return None
        
        paramList = list[dict[str, object]]()
        for k in self.whereParams:
            paramList.append({ "name": k, "value": self.whereParams[k] })

        return paramList


    def __str__(self) -> str:
        formattedWhereParams = "Not defined."

        if self.whereParams is not None and len(self.whereParams) > 0:
            formattedWhereParams = json.dumps(self.whereParams)

        return "'queryStr': '{0}' | 'whereParams': '{1}' | 'enableCrossPartitionQuery': {2}".format(self.queryStr, formattedWhereParams, self.enableCrossPartitionQuery)