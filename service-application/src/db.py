import os
from typing import TypedDict, Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DBClient(TypedDict):
    player_report: Optional[Engine]


db_client: DBClient = {"lendo_db_conn": None}


async def get_db():
    lendo_db_conn = db_client["lendo_db_conn"]

    if not lendo_db_conn:
        USER = os.environ.get("DB_USERNAME", "lendo")
        PASSWORD = os.environ.get("DB_PASSWORD", "lendoab")
        HOST = os.environ.get("DB_HOST", "postgres")
        PORT = os.environ.get("DB_PORT", 5432)
        DATABASE = os.environ.get("DB_NAME", "lendo")

        SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

        conn = create_engine(
            SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
        )

        db_client["lendo_db_conn"] = conn

    return db_client["lendo_db_conn"]


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_db())

Base = declarative_base()
