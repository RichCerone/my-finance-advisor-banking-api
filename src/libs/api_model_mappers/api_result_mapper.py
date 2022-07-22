import logging as logger

from src.libs.api_models.ApiResult import ApiResult

def map_to_api_result(content: any, results: int, page: int) -> ApiResult:
    """
    Maps the content to an API result.

    Parameters
    ----------
    content: any
        Object to return from the API.

    results: int
        Number of results in this API call.

    page: int
        Page number of current results.

    Raises
    ----------
    TypeError
        Raised if a given parameters is invalid..
    """

    try:
        if content is None:
            raise ValueError("'content' must be defined and not empty.")

        if results is None:
            raise TypeError("'results' must be defined.")

        if page is None:
            raise TypeError("'page' must be defined.")

        result = ApiResult(content=content, results=results, page=page)
        return result

    except Exception as e:
        logger.exception("map_to_api_result exception -> An error occurred mapping the API result: {0}".format(e))
        raise