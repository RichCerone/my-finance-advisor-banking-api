
class ApiResult:
    """
    Represents a generic API result containing the detailed results.

    Remarks
    -------
    This should only be used for returning content on successful status codes.
    """
    def __init__(self, content: list = list(), results: int = 0, page: int = 0):
        """
        content: list
            content returned from the API.

        results: int
            The number of results returned from the API.

        page: int
            The current page number where the results were retrieved.
        """

        self.content = content
        self.results = results,
        self.page = page
