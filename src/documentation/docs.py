__all__ = [
    "app_title",
    "description",
    "version",
    "tags_metadata",
    "get_accounts_responses",
    "post_accounts_responses"
]

app_title = "My Finance Advisor Banking API"
version = "0.0.2-alpha"

description = """
**This is the My Finance Advisor Banking API. It handles actions such as:**
### - Managing Accounts
"""

tags_metadata = [
    {
        "name": "accounts",
        "description": "Manages accounts."
    }
]

get_accounts_responses = {
    400: {
        "description": "Parameters are invalid.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    401: {
        "description": "Access Denied.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    404: {
        "description": "No accounts found based on search parameters.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    500: {
        "description": "Error occurred getting accounts or unexpected error.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    }
}

post_accounts_responses = {
    400: {
        "description": "Parameters are invalid.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    401: {
        "description": "Access Denied.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    409: {
        "description": "Account already exists.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    },
    500: {
        "description": "Error occurred getting accounts or unexpected error.",
        "content": {
            "application/json": {
                "example": {"status_code": 0, "detail": "string"}
            }
        }
    }
}