from fastapi import Depends, FastAPI, Request, HTTPException
from src.routers import accounts

app = FastAPI()

app.include_router(accounts.router)