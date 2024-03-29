import json

from fastapi.testclient import TestClient
from src.libs.api_models.AccountModel import AccountModel
from src.main import app
from src.routers.accounts import authorize_access, accounts_db, inject_jwt_bearer
from src.data_models.Account import Account
from unittest.mock import Mock

# Setup
def init_inject_jwt_bearer_authenticates():
    return "some_token"


def init_authorize_access_returns_user():
    return "some_user"


def init_accounts_db_gets_account():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = json.dumps(Account("1234", "some_account_name", "some_account_type", "some_bank", "some_owner", "1000.00").__dict__)

    return accounts_db_mock


def init_accounts_db_gets_account_returns_none():
    accounts_db_mock = Mock()
    accounts_db_mock.get.return_value = None

    return accounts_db_mock


def init_accounts_db_gets_account_raises_exception():
    accounts_db_mock = Mock()
    accounts_db_mock.get.side_effect = Exception()

    return accounts_db_mock


def init_accounts_db_queries_accounts():
    accounts_db_mock = Mock()

    accounts = list()
    
    for i in range(2):
        accounts.append(Account(i.__str__(), "some_account_name", "some_account_type", "some_bank", "some_owner", "1000.00").__dict__)

    accounts_db_mock.query.return_value = json.dumps(accounts)

    return accounts_db_mock


client = TestClient(app)

# Test
# Asserts a 200 status code is returned.
def test_get_account_returns_200():
    app.dependency_overrides[authorize_access] = init_authorize_access_returns_user
    app.dependency_overrides[accounts_db] = init_accounts_db_gets_account
    app.dependency_overrides[inject_jwt_bearer] = init_inject_jwt_bearer_authenticates

    # Test get by key.
    response = client.get("/accounts?id={0}".format("account::1234"))

    assert response.status_code == 200
    
    content = response.json()
    account = AccountModel(**content["content"])

    assert type(account) == AccountModel
    assert account.account_id == "1234"

    # Test get by query.
    app.dependency_overrides[accounts_db] = init_accounts_db_queries_accounts

    response = client.get("/accounts?account_name={0}".format("some_account_name"))

    assert response.status_code == 200

    content = response.json()
    accounts = content["content"]

    assert type(accounts) == list
    assert len(accounts) == 2
    
    account = AccountModel(**accounts[0])

    assert type(account) == AccountModel
    assert account.account_id == "0"


# Asserts a 400 status code is returned.
def test_get_returns_400():
    response = client.get("/accounts?id={0}".format(" "))

    assert response.status_code == 400


# Asserts a 403 status code is returned.
def test_get_returns_403():
    app.dependency_overrides = {}

    response = client.get("/accounts?account_name={0}".format("some_account_name"))

    assert response.status_code == 403
    

# Asserts a 404 status code is returned.
def test_get_returns_404():
    app.dependency_overrides[authorize_access] = init_authorize_access_returns_user
    app.dependency_overrides[inject_jwt_bearer] = init_inject_jwt_bearer_authenticates
    app.dependency_overrides[accounts_db] = init_accounts_db_gets_account_returns_none

    response = client.get("/accounts?id={0}".format("account::1234"))

    assert response.status_code == 404


# Asserts a 500 status code is returned.
def test_get_returns_500():
    app.dependency_overrides[accounts_db] = init_accounts_db_gets_account_raises_exception

    response = client.get("/accounts?id={0}".format("account::1234"))

    assert response.status_code == 500