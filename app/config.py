from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    class Config:
        env_file = ".env"

settings = Settings()
print(f"Database Username: {settings.database_username}")
print(f"Database Password: {settings.database_password}")