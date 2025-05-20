import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from snack_bar_system.models import table_registry  # substitua pelo seu Base real


@pytest.fixture(scope='session')
def postgres_container():
    """Inicializa um container PostgreSQL temporário com testcontainers."""
    with PostgresContainer('postgres:15') as postgres:
        engine = create_engine(postgres.get_connection_url())
        table_registry.metadata.create_all(engine)
        yield engine
        engine.dispose()


@pytest.fixture
def db_session(postgres_container):
    """Cria uma sessão com rollback automático para cada teste."""
    connection = postgres_container.connect()
    transaction = connection.begin()

    session = Session(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()
