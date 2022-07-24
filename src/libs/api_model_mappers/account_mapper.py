import logging as logger

from src.libs.api_models.AccountModel import AccountModel

def map_to_account_api_model(payload: dict[str, any]) -> AccountModel:
    """
    Maps the account data model to the account API model.

    Parameters
    ----------
    payload: dict[str, any]
        The JSON object converted from the JSON string.

    Returns
    -------
    Account
        The account object mapped to.

    Raises
    ------
    TypeError
        Raised if the payload passed is None.
    """

    try:
        logger.debug("Checking if JSON payload is valid.")

        if payload is None:
            raise TypeError("Cannot map empty JSON payload to model.")

        logger.debug("JSON payload is valid: '{0}'".format(payload))
        logger.debug("Converting JSON payload to account model.")

        # Map data model to API model.
        account = AccountModel()
        
        account.account_id = payload["account_id"]
        account.account_name = payload["account_name"]
        account.account_type = payload["account_type"]
        account.account_institution = payload["account_institution"]
        account.balance = payload["balance"]

        logger.debug("Payload converted to account model: {0}".format(account.__str__()))

        return account

    except Exception as e:
        logger.exception("map_to_account_api_model exception -> Error mapping account data: {0}".format(e))
        raise


def map_to_account_api_models(payload: list[dict[str, any]]) -> list:
    """
    Map the account data model to an account API model.

    Parameters
    ----------
    payload: list[dict[str, any]]
        The JSON objects converted from the JSON string.

    Returns
    -------
    list
        The account objects mapped to.

    Raises
    ------
    TypeError
        Raised if the payload passed is None.
    """

    try:
        if payload is None or payload.__len__() == 0:
            raise TypeError("The payload must be defined and not empty.")

        accounts = list()
        for obj in payload:
            account = map_to_account_api_model(obj)
            accounts.append(account)
        
        return accounts

    except Exception as e:
        logger.error("map_to_account_api_models exception -> An error occurred mapping multiple account models: {0}".format(e))
        raise