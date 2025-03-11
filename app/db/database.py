from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
#cambiar usuario y nombre de la bd!!!
DATABASE_URL = "mysql+asyncmy://root:12345678@127.0.0.1:3306/db_sleep_quality"
engine = create_async_engine(DATABASE_URL)
session_local = sessionmaker(autoflush=False,bind=engine,class_=AsyncSession,expire_on_commit=False)

class Base(DeclarativeBase):
  pass

# Función para obtener la sesión de la base de datos
async def get_db() -> AsyncSession:
    async with session_local() as session:
        yield session