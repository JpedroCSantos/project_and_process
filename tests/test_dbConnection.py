import pytest
import psycopg2

from datetime import date
from src.config.config import settings

def test_connect_db() -> str:
    params = settings.dev_db_params
    
    with psycopg2.connect(**params) as conn:
        assert conn is not None