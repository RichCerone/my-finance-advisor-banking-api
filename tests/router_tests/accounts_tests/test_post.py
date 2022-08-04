import json

from fastapi.testclient import TestClient
from src.libs.api_models.AccountModel import AccountModel
from src.main import app
from src.routers.accounts import authorize_access, accounts_db, inject_jwt_bearer
from src.data_models.Account import Account
from unittest.mock import Mock

# Setup
def init_inject_jwt_bearer_authenticates():
    inject_jwt_bearer_mock = Mock()
    inject_jwt_bearer_mock.return_value = "some_token"

    return inject_jwt_bearer_mock


def init_authorize_access_returns_user():
    return "some_user"


def init_accounts_db_get_returns_account():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = json.dumps(Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", "1000.00").__dict__)

    return accounts_db_mock


def init_accounts_db_upserts_account():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = None
    accounts_db_mock.upsert.return_value = json.dumps(Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", "1000.00").__dict__)

    return accounts_db_mock


def init_accounts_db_get_raises_exception():
    accounts_db_mock = Mock()
    accounts_db_mock.get.side_effect = Exception()

    return accounts_db_mock


client = TestClient(app)

# Test
# Assert post returns a 201 status code.
def test_post_returns_201():
    app.dependency_overrides[authorize_access] = init_authorize_access_returns_user
    app.dependency_overrides[accounts_db] = init_accounts_db_upserts_account
    app.dependency_overrides[inject_jwt_bearer] = init_inject_jwt_bearer_authenticates

    account = AccountModel()
    account.account_id = "1234"
    account.account_name = "some_name"
    account.account_type = "some_type"
    account.account_institution = "some_bank"
    account.balance = "1000.00"

    payload = json.dumps(account.__dict__)

    response = client.post("/accounts/", json=json.loads(payload))

    assert response.status_code == 201
    
    content = response.json()
    result = content["content"]

    account = AccountModel(**result)

    assert type(account) == AccountModel
    assert account.account_id == "1234"


# Asserts a 400 status code is returned.
def test_post_returns_400():
    account = AccountModel()
    account.account_id = " "
    account.account_name = "some_name"
    account.account_type = "some_type"
    account.account_institution = "some_bank"
    account.balance = "1000.00"

    payload = json.dumps(account.__dict__)

    response = client.post("/accounts/", json=json.loads(payload))

    assert response.status_code == 400

# Asserts a 409 status code is returned.
def test_post_returns_409():
    app.dependency_overrides[accounts_db] = init_accounts_db_get_returns_account

    account = AccountModel()
    account.account_id = "1234"
    account.account_name = "some_name"
    account.account_type = "some_type"
    account.account_institution = "some_bank"
    account.balance = "1000.00"

    payload = json.dumps(account.__dict__)

    response = client.post("/accounts/", json=json.loads(payload))

    assert response.status_code == 409


def test_post_returns_500():
    app.dependency_overrides[accounts_db] = init_accounts_db_get_raises_exception

    account = AccountModel()
    account.account_id = "1234"
    account.account_name = "some_name"
    account.account_type = "some_type"
    account.account_institution = "some_bank"
    account.balance = "1000.00"

    payload = json.dumps(account.__dict__)

    response = client.post("/accounts/", json=json.loads(payload))

    assert response.status_code == 500