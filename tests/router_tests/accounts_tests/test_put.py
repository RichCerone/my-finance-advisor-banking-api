import json

from fastapi.testclient import TestClient
from src.libs.api_models.AccountModel import AccountModel
from src.libs.api_models.UpdateAccountModel import UpdateAccountModel
from src.main import app
from src.routers.accounts import authorize_access, accounts_db, inject_jwt_bearer
from src.data_models.Account import Account
from unittest.mock import Mock

# Setup.
def init_inject_jwt_bearer_authenticates():
    return "some_token"


def init_authorize_access_returns_user():
    return "user"


def init_accounts_db_get_returns_none():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = None

    return accounts_db_mock


def init_accounts_db_upserts_account():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = json.dumps(Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", "1000.00").__dict__)
    accounts_db_mock.upsert.return_value = json.dumps(Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", "2000.00").__dict__)

    return accounts_db_mock


def init_accounts_db_get_raises_exception():
    accounts_db_mock = Mock()
    accounts_db_mock.get.side_effect = Exception()

    return accounts_db_mock


client = TestClient(app)

# Test
# Assert a 200 status code is returned.
def test_put_returns_200():
    app.dependency_overrides[authorize_access] = init_authorize_access_returns_user
    app.dependency_overrides[accounts_db] = init_accounts_db_upserts_account
    app.dependency_overrides[inject_jwt_bearer] = init_inject_jwt_bearer_authenticates

    account_to_update = UpdateAccountModel()
    account_to_update.account_id = "1234"
    account_to_update.account_name = "some_account_name"
    account_to_update.balance = "2000.00"

    payload = json.dumps(account_to_update.__dict__)

    response = client.put("/accounts/", json=json.loads(payload))

    assert response.status_code == 200
    
    content = response.json()
    result = content["content"]

    account = AccountModel(**result)

    assert type(account) == AccountModel
    assert account.balance == "2000.00"


# Asserts a 400 status code is returned.
def test_put_returns_400():
    account_to_update = UpdateAccountModel()
    account_to_update.account_id = " "
    account_to_update.account_name = "some_account_name"
    account_to_update.balance = "2000.00"

    payload = json.dumps(account_to_update.__dict__)

    response = client.put("/accounts/", json=json.loads(payload))

    assert response.status_code == 400


# Asserts a 404 status code is returned.
def test_put_returns_404():
    app.dependency_overrides[accounts_db] = init_accounts_db_get_returns_none

    account_to_update = UpdateAccountModel()
    account_to_update.account_id = "1234"
    account_to_update.account_name = "some_account_name"
    account_to_update.balance = "2000.00"

    payload = json.dumps(account_to_update.__dict__)

    response = client.put("/accounts/", json=json.loads(payload))

    assert response.status_code == 404
    

# Asserts a 500 status code is returned.
def test_put_returns_500():
    app.dependency_overrides[accounts_db] = init_accounts_db_get_raises_exception

    account_to_update = UpdateAccountModel()
    account_to_update.account_id = "1234"
    account_to_update.account_name = "some_account_name"
    account_to_update.balance = "2000.00"
    
    payload = json.dumps(account_to_update.__dict__)

    response = client.put("/accounts/", json=json.loads(payload))

    assert response.status_code == 500