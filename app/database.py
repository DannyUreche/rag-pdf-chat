import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Am actualizat credențialele cu rag_user:rag_password exact ca în docker-compose.yml
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://rag_user:rag_password@localhost:5432/rag_db"
)

# Creăm motorul asincron pentru PostgreSQL
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Generatorul de sesiuni asincrone folosit și de FastAPI, și de Celery
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Dependency pentru rutele FastAPI
async def get_db():
    async with async_session_maker() as session:
        yield session