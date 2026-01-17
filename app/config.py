from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_NAME: str = "students_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    # FastAPI настройки
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_RELOAD: bool = True  
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()