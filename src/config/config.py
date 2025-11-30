import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv(override=False)

load_env()

@dataclass(frozen=False)
class Settings:
    dev_db_params: Dict[str, any] = field(default_factory=lambda: {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", "5432")),
        "dbname": os.getenv("PG_DATABASE", "trips_analysis"),
        "user": os.getenv("PG_USER", "etl_process"),
        "password": os.getenv("PG_PASSWORD", "postgres")
    })
    
settings = Settings()