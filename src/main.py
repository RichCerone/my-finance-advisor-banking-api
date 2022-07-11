from fastapi import FastAPI
from src.routers import accounts

app = FastAPI()

app.include_router(accounts.router)