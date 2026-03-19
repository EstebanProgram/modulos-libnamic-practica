import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.base import Base  # tu base declarativa de SQLAlchemy

# Configuración de la base de datos de tests
DB_USER = os.getenv("DB_USER", "licium")
DB_PASSWORD = os.getenv("DB_PASSWORD", "licium_dev_password")
DB_HOST = os.getenv("DB_HOST", "postgres")  # nombre del contenedor o host
DB_NAME = os.getenv("DB_TEST_NAME", "licium_test")  # base de datos de tests ya creada

TEST_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL)
    return engine


@pytest.fixture(scope="session")
def tables(engine):
    # Crear todas las tablas antes de los tests
    Base.metadata.create_all(bind=engine)
    yield
    # Limpiar las tablas después de la sesión de tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(engine, tables):
    """Provee una sesión limpia para cada test."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.rollback()  # revertir cambios tras cada test
    finally:
        session.close()