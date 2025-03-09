from logging.config import fileConfig
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.database import Base 
from alembic import context
import sys
import os

# Alembic Config object
config = context.config

# Configurar el logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Añadir tus modelos aquí para la autogeneración
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app.models import data, dailyReport, smartwatch, user, userType

# Metadata de tus modelos
target_metadata = Base.metadata


# Función para migraciones offline
def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Función para migraciones online asincrónicas
async def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online (asincrónico)."""

    # Crear la conexión asíncrona usando el driver asyncmy
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
        pool_pre_ping=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# Función para ejecutar migraciones
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


# Detectar si es modo offline u online
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
