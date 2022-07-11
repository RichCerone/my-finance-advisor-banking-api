
class Entity:
    """
    A generic data entity which would store data.
    """    

    def __init__(self, collection_name: str):
        """
        Creates a new data entity.

        collection_name: str
            The name of the collection this entity belongs to.
            Will be used as a partial identifier for entity's
            full identifier.
        """

        self.id = ""
        self._rid = "",
        self._self = ""
        self._etag = "",
        self._attachments = "",
        self._ts = 0
        self.collection_name = collection_name


    def create_id(self, id: str):
        """
        Creates a new id for the object.

        Parameters
        ----------
        id: str
            The id which will be the partial makeup of the whole identifier.

        Returns
        -------
        str
            The new id.

        Raises
        ------
        ValueError
            Raised if the parameter given is invalid.

        Remarks
        -------
        When calling this method, the id for this class will also be assigned
        with the new id created. There is no need to assign the new id to 'self.id'.
        """

        if not id or id.isspace():
            raise ValueError("identifier must be defined.")

        self.id = "".join(id.split())
        self.id = "{0}::{1}".format(self.collection_name, self.id.lower())
        
        return self.id