from src.data_models.Entity import Entity

_collection_name = "user"

class User(Entity):
    """
    Holds the user data.
    """

    def __init__(self, user: str, password: str):
        """
        Creates a new User.

        Parameters
        ----------
        user: str
            The username. Spaces will be stripped.
        
        password: str
            The hashed password for this user.

        Raises
        ------
        ValueError
            Raised if the user or password is not defined.
        """

        super().__init__(_collection_name)

        if not password or password.isspace():
            raise ValueError("password must be defined.")

        self.id = self.create_id(user)
        self.user = user
        self.password = password


    def __str__(self) -> str:
        return "'id': '{0}' | 'user': '{1}'".format(self.id, self.user)
