import unittest

from decimal import Decimal
from src.libs.api_model_mappers.account_mapper import map_to_account_api_model
from src.data_models.Account import Account
from src.libs.api_models.AccountModel import AccountModel

class MapToAccountApiModelTests(unittest.TestCase):
    # Assert that an account data model maps to an account API model.
    def test_map_to_account_api_model_maps(self):
        payload = Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", Decimal("1000.00")).__dict__
        
        with self.assertLogs(level="DEBUG"):
            result = map_to_account_api_model(payload)

        self.assertEqual(AccountModel, type(result))
        self.assertEqual("1234", result.account_id)
        self.assertEqual("some_account_name", result.account_name)
        self.assertEqual("some_account_type", result.account_type)
        self.assertEqual("some_bank", result.account_institution)
        self.assertEqual(Decimal("1000.00"), result.balance)


    # Assert that a TypeError is raised if the payload is None.
    def test_map_to_account_api_model_raises_type_error(self):
        payload = None

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_account_api_model(payload)