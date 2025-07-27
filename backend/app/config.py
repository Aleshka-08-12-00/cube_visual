from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    adomd_connection: str
    adomd_dll_path: str | None = None
    cors_origins: List[str] = ["*"]
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), "..", ".env"), env_file_encoding="utf-8", extra="ignore")

settings = Settings()
