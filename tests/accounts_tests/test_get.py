from http.client import HTTPException
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import Mock

def init_authorize_access_returns_user():
    authorize_access_mock = Mock()
    authorize_access_mock.return_value = "some_user"

    return authorize_access_mock


def init_authorize_access_returns_unauthorized():
    authorize_access_mock = Mock()
    authorize_access_mock.side_effect = HTTPException(403)

client = TestClient(app)

