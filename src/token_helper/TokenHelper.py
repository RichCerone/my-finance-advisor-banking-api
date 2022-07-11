import logging as logger

from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError, JWTClaimsError, ExpiredSignatureError
from src.token_helper.exceptions.CredentialNotInJwtError import CredentialNotInJwtError

class TokenHelper():
    """
    Helps generate and authorize tokens.
    """

    def __init__(self, secret_key: str, algo: str, access_token_expire_minutes: int=30):
        """
        Parameters
        ----------
        secret_key: str
            The secret key used for signing the token.

        algo: str
            The algorithm to use for signing the token.

        access_token_expire_minutes: int
            Time in minutes the token expires. Default is 30 minutes.

        Raises
        ------
        ValueError
            Raised if the secret key or algorithm are undefined.
        """

        if secret_key is None or secret_key.isspace():
            raise ValueError("secret_key must be defined.")
        
        elif algo is None or algo.isspace():
            raise ValueError("algo must be defined.")

        self.secret_key = secret_key
        self.algo = algo
        self.access_token_expire_minutes = access_token_expire_minutes


    def create_access_token(self, data: dict, expires: bool=True) -> str:
        """
        Creates the access token.

        Parameters
        ----------
        data: dict
            The data to encode into the token.

        expires: bool
            Whether this token should expire.

        Returns
        -------
        any
            The token.

        Raises
        -----
        JWTError:
            Raised if the token cannot be encoded.

        Exception:
            Raised if an unexpected error occurs.
        """
        try:
            logger.debug("Copying data to encode.")

            to_encode = data.copy()

            logger.debug("Data copied. Checking if token needs to expire.")

            if expires:
                logger.debug("Token will expire in {0} minutes".format(self.access_token_expire_minutes))

                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

                logger.debug("Updating data to include expiration datetime.")

                to_encode.update({ "exp": expire })

            logger.debug("Encoding token.")

            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algo)

            logger.debug("Token encoded.")

            return encoded_jwt

        except JWTError as e:
            logger.exception("create_access_token exception -> Error occurred during encoding: {0}".format(e))
            raise
        except Exception as e:
            logger.exception("create_access_token exception -> Error occurred creating the token: {0}".format(e))
            raise

    def decode_access_token(self, token: str) -> str:
        """
        Decodes the access token.

        Parameters
        ----------
        token: str
            The token to decode.

        Raises
        -----
        JWTClaimsError:
            Raised if the claim in the token is invalid.

        ExpiredSignatureError:
            Raised if the signature signing the token is invalid.

        JWTError:
            Raised if the token cannot be decoded.

        Exception:
            Raised if an unexpected error occurs.

        Returns
        -------
        str:
            The username in the token.
        """
        
        try:
            logger.debug("Decoding token: '{0}'".format(token))

            payload = jwt.decode(token, self.secret_key, algorithms=[self.algo])

            logger.debug("Token decoded. Retrieving username payload.")

            username: str = payload.get("sub")
            if username is None or username.isspace():
                logger.error("Username payload is not defined.")
                raise CredentialNotInJwtError("Expected 'sub' credential in the payload, but it was not found.")

        except JWTClaimsError as e:
            logger.exception("decode_access_token exception -> The claim in the token is invalid: {0}".format(e))
            raise

        except ExpiredSignatureError as e:
            logger.exception("decode_access_token exception -> The signature is invalid: {0}".format(e))
            raise

        except JWTError as e:
            logger.exception("decode_access_token exception -> cannot decode token: {0}".format(e))
            raise

        except Exception as e:
            logger.exception("decode_access_token exception -> An error occurred trying to decode the token: {0}".format(e))
            raise
        
        logger.debug("username extracted from token.")
        
        return username
    
    
    