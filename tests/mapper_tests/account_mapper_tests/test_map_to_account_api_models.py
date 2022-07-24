from decimal import Decimal
import unittest

from src.libs.api_model_mappers.account_mapper import map_to_account_api_models
from src.data_models.Account import Account
from src.libs.api_models.AccountModel import AccountModel

class MapToAccountApiModelsTests(unittest.TestCase):
    # Assert that multiple account models are mapped to multiple account API models.
    def test_map_to_account_api_models(self):
        payload = list()

        for i in range(2):
            payload.append(Account(i.__str__(), "some_account_name", "some_account_type", "some_bank", Decimal("1000.00")).__dict__)

        with self.assertLogs(level="DEBUG"):
            result = map_to_account_api_models(payload)

        self.assertEqual(2, result.__len__())
        self.assertEqual(AccountModel, type(result[0]))

    
    # Asserts that a TypeError is raised if the payload is none or empty.
    def test_map_to_account_api_models_raises_type_error(self):
        # Case 1: Payload is None.
        payload = None

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_account_api_models(payload)

        # Case 2: Payload is empty.
        payload = list()

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_account_api_models(payload)
        