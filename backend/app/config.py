from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

# Determine which environment file to load. By default we try ``.env``. If it
# does not exist fall back to ``.env.example`` so the application can start
# with the sample configuration. Users can still override values using real
# environment variables or by creating their own ``.env`` file.
_env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
if not os.path.exists(_env_file):
    example_file = os.path.join(os.path.dirname(__file__), "..", ".env.example")
    if os.path.exists(example_file):
        _env_file = example_file

class Settings(BaseSettings):
    adomd_connection: str
    adomd_dll_path: str | None = None
    cors_origins: str = "*"

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list."""
        v = self.cors_origins.strip()
        if not v:
            return []
        if v.startswith("["):
            import json
            try:
                return json.loads(v)
            except Exception:
                pass
        return [item.strip() for item in v.split(",") if item.strip()]
        

    model_config = SettingsConfigDict(env_file=_env_file, env_file_encoding="utf-8", extra="ignore")

settings = Settings()
