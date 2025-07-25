from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    xmla_url: str = ""
    xmla_username: str = ""
    xmla_password: str = ""
    xmla_catalog: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
