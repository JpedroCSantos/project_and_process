import pytest
import psycopg2

from datetime import date
from src.config.config import settings
from sqlalchemy import create_engine, text

def test_connect_db() -> str:
    params = settings.dev_db_params
    
    with psycopg2.connect(**params) as conn:
        assert conn is not None

def test_connect_sqlalchemy():
    """
    Testa se a engine do SQLAlchemy consegue conectar e executar uma query.
    """
    params = settings.dev_db_params
    connection_string = f'postgresql://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["dbname"]}'
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1