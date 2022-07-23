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
        logger.debug("Validating 'content' parameter.")

        if content is None:
            raise ValueError("'content' must be defined and not empty.")

        logger.debug("'content' is valid.")
        logger.debug("Validating 'results' parameter.")

        if results is None:
            raise TypeError("'results' must be defined.")

        logger.debug("'results' parameter valid.")
        logger.debug("Validating 'page' parameter.")

        if page is None:
            raise TypeError("'page' must be defined.")

        logger.debug("'page' parameter valid.")
        logger.debug("Creating API result")

        result = ApiResult(content=content, results=results, page=page)

        logger.debug("API results created.")

        return result

    except Exception as e:
        logger.exception("map_to_api_result exception -> An error occurred mapping the API result: {0}".format(e))
        raise