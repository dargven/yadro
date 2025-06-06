import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import models and Base
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.database import Base, SYNC_DATABASE_URL
from app.users.models import User

# Get Alembic config
config = context.config
fileConfig(config.config_file_name)

if not SYNC_DATABASE_URL:
    raise ValueError("SYNC_DATABASE_URL must be set for Alembic migrations")

config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)
target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
