import unittest
from src.data_models.Account import Account

from src.libs.api_models.AccountModel import AccountModel
from src.libs.api_model_mappers.account_mapper import map_to_account_data_model

class MapToAccountDataModelTests(unittest.TestCase):
    def setUp(self):
        self.account_api_model = AccountModel()
        self.account_api_model.account_id = "some_id"
        self.account_api_model.account_name = "some_name"
        self.account_api_model.account_type= "some_type"
        self.account_api_model.account_institution = "some_bank"
        self.account_api_model.balance = "1000.00"


    def tearDown(self) -> None:
        self.account_api_model = None
        

    # Assert account API model maps to account data model.
    def test_map_to_account_data_model(self):
        with self.assertLogs(level="DEBUG"):
            account = map_to_account_data_model(self.account_api_model)

        self.assertEqual(Account, type(account))
        self.assertEqual("account::some_id", account.id)


    # Assert a type error is raised if the account is None.
    def test_map_to_account_data_model_raises_type_error(self):
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(TypeError):
                map_to_account_data_model(None)
        