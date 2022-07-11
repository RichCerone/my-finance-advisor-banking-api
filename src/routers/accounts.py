from fastapi import APIRouter, Depends
from src.libs.utils.authorize import authorize_access
from src.authorization.JwtBearer import inject_jwt_bearer

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[
        Depends(inject_jwt_bearer)
    ]
)

@router.get("/")
def get(user: str = Depends(authorize_access)):
    return user