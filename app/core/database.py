from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
import os

# Создаем асинхронный движок с учетом типа БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Проверка соединения перед использованием
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Асинхронная сессия
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Dependency для получения сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()