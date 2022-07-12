from fastapi import FastAPI
from src.routers import accounts
from src.documentation.docs import *

app = FastAPI(
    title=app_title,
    description=description,
    version=version,
    openapi_tags=tags_metadata
)

app.include_router(accounts.router)