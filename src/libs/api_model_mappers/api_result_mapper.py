import logging as logger

from src.libs.api_models.ApiResult import ApiResult

def map_to_api_result(content: list, results: int, page: int) -> ApiResult:
    
    try:
        if content is None or content.__len__ == 0:
            raise ValueError("'content' must be defined and not empty.")

        if results is None:
            raise TypeError("'results' must be defined.")

        if page is None:
            raise TypeError("'page' must be defined.")

        result = ApiResult(content, results, page)
        return result

    except Exception as e:
        logger.exception("map_to_api_result exception -> An error occurred mapping the API result: {0}".format(e))
        raise