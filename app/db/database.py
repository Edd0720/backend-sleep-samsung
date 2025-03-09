from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
#cambiar usuario y nombre de la bd!!!
DATABASE_URL = "mysql+asyncmy://root:Harry200412*@127.0.0.1:3306/db_sleep_quality"
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,bind=engine)

class Base(DeclarativeBase):
  pass

