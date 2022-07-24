from pydantic import BaseModel

class ApiResult(BaseModel):
    """
    Represents a generic API result containing the detailed results.

    Parameters
    ----------
    content: object
        content returned from the API.

    results: int
        The number of results returned from the API.

    page: int
        The current page number where the results were retrieved.

    Remarks
    -------
    This should only be used for returning content on successful status codes.
    """

    content: object = None
    results: int = 0
    page: int = 0
