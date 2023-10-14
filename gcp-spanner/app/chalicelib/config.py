from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    instance_id: str
    database_id: str
    credentials_path: str

    class Config:
        env_file = ".env"
