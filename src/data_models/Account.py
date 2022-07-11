from src.data_models.Entity import Entity
from decimal import Decimal

_collection_name = "account"

class Account(Entity):
    """
    Holds the account data.
    """

    def __init__(self, account_id: str, account_name: str = "", account_type: str = "", account_institution: str = "", balance: Decimal = Decimal("0.00")):
        """
        Creates a new account.
        
        Parameters
        ----------
        account_id: str
            The id of the account.

        account_name: str
            The name of the account.

        account_type: str
            The type of account.

        account_institution: str
            The institution that manages this account.

        balance: Decimal
            The monetary balance on this account.

        Raises
        ------
        ValueError
            Raised if the account_id, account_name, account_type, or account_institution are undefined.

        TypeError
            Raised if the amount is undefined.
        """

        super().__init__(_collection_name)

        self.__validate_params(account_id, account_name, account_type, account_institution, balance)

        self.id = self.create_id(account_id)
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        self.account_institution = account_institution
        self.balance = balance


    def __validate_account_id(self, account_id: str):
        if not account_id or account_id.isspace():
            raise ValueError("'account_id' must be defined.")


    def __validate_params(self,account_id: str, account_name: str, account_type: str, account_institution: str, balance: Decimal):
        self.__validate_account_id(account_id)

        if (not account_name or account_name.isspace()) and account_name != "":
            raise ValueError("'account_name' must be defined.")

        if (not account_type or account_type.isspace()) and account_type != "":
            raise ValueError("'account_type' must be defined.")

        if (not account_institution or account_institution.isspace()) and account_institution != "":
            raise ValueError("'account_institution' must be defined.")

        if balance == None:
            raise TypeError("'balance' must be defined.")


    def __str__(self) -> str:
        return "'id': '{0}' | 'account_id': '{1}' | 'account_name': '{2}' | 'account_type': '{3}' | 'account_institution': '{4}' | 'balance': '${5}'".format(self.id, self.account_id, self.account_name, self.account_type, self.account_institution, self.balance)