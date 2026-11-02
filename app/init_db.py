import asyncio
from sqlalchemy import text
from app.database import engine, Base
import app.models  # Încarcă modelele pentru ca Base să le recunoască


async def init_models():
    async with engine.begin() as conn:
        # Activăm extensia vector în PostgreSQL
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))

        # Creăm toate tabelele definite în models.py
        await conn.run_sync(Base.metadata.create_all)

    print(" Baza de date a fost inițializată cu succes și extensia pgvector este activă!")


if __name__ == "__main__":
    asyncio.run(init_models())