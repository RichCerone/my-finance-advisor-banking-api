import unittest

from src.libs.api_model_mappers.api_result_mapper import map_to_api_result
from src.libs.api_models.ApiResult import ApiResult

class MapToApiResultTests(unittest.TestCase):
    # Assert that content is mapped to an API result model.
    def test_map_to_api_result_maps(self):
        with self.assertLogs(level="DEBUG"):
            result = map_to_api_result("some_content", 1, 1)

        self.assertEqual(ApiResult, type(result))
        self.assertEqual("some_content", result.content)
        self.assertEqual(1, result.results)
        self.assertEqual(1, result.page)


    # Asserts that a ValueError is raised if the content is invalid.
    def test_map_to_api_result_raises_value_error(self):
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(ValueError):
                map_to_api_result(None, 1, 1)


    # Asserts that a TypeError is raised if the results or page are invalid.
    def test_map_to_api_result_raises_type_error(self):
        # Case 1: results is None.
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_api_result("some_content", None, 1)

        # Case 2: page is None.
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_api_result("some_content", 1, None)