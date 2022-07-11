from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


class JWTBearer(HTTPBearer):
    """
    JWT Bearer middleware for processing JWT tokens in the HTTP request header.
    """
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            return credentials.credentials
            
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

# This is used when you want to inject the caller as a dependency. This way it can be mocked during testing.
inject_jwt_bearer = JWTBearer()