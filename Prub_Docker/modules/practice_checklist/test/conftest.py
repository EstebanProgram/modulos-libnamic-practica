import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.base import Base 

# Configuración
DB_USER = os.getenv("DB_USER", "licium")
DB_PASSWORD = os.getenv("DB_PASSWORD", "licium_dev_password")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_TEST_NAME", "licium_test")

TEST_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL, pool_pre_ping=True)

@pytest.fixture(scope="session")
def tables(engine):
    """Limpia el esquema y crea tablas ignorando errores de duplicados."""
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))
        conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
        conn.commit()
    
    # Intentamos crear. Si el índice ya existe por un doble import, lo ignoramos.
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        if "already exists" in str(e):
            pass # Ignoramos el error de duplicado y seguimos
        else:
            raise e
    yield

@pytest.fixture()
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()