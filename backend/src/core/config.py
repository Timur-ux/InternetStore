from pathlib import Path
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from async_fastapi_jwt_auth import AuthJWT

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    
    project_name: str = Field(
        "InternetStore API", alias="PROJECT_NAME", env="PROJECT_NAME"
    )
    base_dir: str = str(Path(__file__).parent.parent)
    postgres_conn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:password@localhost:5432/internetstore",
        alias="DATABASE_CONN",
        env="DATABASE_CONN",
    )
    echo: bool = Field(True, alias="ECHO", env="ECHO")
    
    # Перенести в .env
    secret_key: str = Field("your_secret_key_here", alias="SECRET_KEY", env="SECRET_KEY")
    
    # Настройки для AuthJWT
    authjwt_secret_key: str = Field("your_secret_key_here", alias="AUTHJWT_SECRET_KEY", env="AUTHJWT_SECRET_KEY")
    authjwt_token_location: set = Field({"cookies"}, alias="AUTHJWT_TOKEN_LOCATION", env="AUTHJWT_TOKEN_LOCATION")

settings = Settings()

# Настройка AuthJWT
@AuthJWT.load_config
def get_config():
    return settings  # Возвращаем экземпляр настроек
