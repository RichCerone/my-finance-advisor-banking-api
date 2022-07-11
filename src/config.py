from pydantic import BaseSettings

class Settings(BaseSettings):
    origins: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30
    endpoint: str
    key: str
    database_id:str
    users_container_id:str
    accounts_container_id: str
    max_page_size: int

    class Config:
        env_file = ".env"