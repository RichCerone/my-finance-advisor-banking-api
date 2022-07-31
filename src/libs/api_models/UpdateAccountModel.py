from pydantic import BaseModel

class UpdateAccountModel(BaseModel):
    """
    Information to update an account.

    Parameters
    ----------
    account_id: str
        The account id to update.

    account_name: str
        The new account name.
    balance: str
        The new balance of the account. 
    """
    
    account_id: str = None
    account_name: str = None
    balance: str = None

    
    def __str__(self) -> str:
        return "'account_id': '{0}' | 'account_name': '{1}' | 'balance': '${2}'".format(self.account_id, self.account_name, self.balance)