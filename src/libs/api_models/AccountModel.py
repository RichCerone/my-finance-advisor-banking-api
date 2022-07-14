
class AccountModel:
    """
    Information about an account.

    Remarks
    -------
    This is an API model used to abstract database specific data.
    """

    def __init__(self, account_id: str = None, account_name: str = None, account_type: str = None, account_institution: str = None, balance: str = "0.00"):
        """
        Creates a new AccountModel.

        Parameters
        ----------
        account_id: str
            The account's id.

        account_name: str
            Name of the account: str.

        account_type: str
            The type of account.

        account_institution: str
            The bank who manages this account.

        balance: str
            The balance in the account.
        """
        
        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type
        self.account_institution = account_institution
        self.balance = balance


    def __str__(self) -> str:
        return "'account_id': {0} | 'account_name': '{1}' | 'account_type': '{2}' | 'account_institution': '{3}' | 'balance': '${4}'".format(self.account_id, self.account_name, self.account_type, self.account_institution, self.balance)
