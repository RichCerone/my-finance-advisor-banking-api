from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@router.get("/")
def get():
    return "hello"