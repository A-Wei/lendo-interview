import asyncio
from pathlib import Path
from typing import TypedDict
import pytest
from testcontainers.postgres import PostgresContainer
from src.db import get_db


class DatabaseFixture(TypedDict):
    host: str
    port: int
    database: str
    username: str
    password: str
    connection_url: str


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def mock_settings(monkeypatch, database: DatabaseFixture):
    monkeypatch.setenv("DB_HOST", database["host"])
    monkeypatch.setenv("DB_PORT", str(database["port"]))
    monkeypatch.setenv("DB_USERNAME", database["username"])
    monkeypatch.setenv("DB_PASSWORD", database["password"])
    monkeypatch.setenv("DB_NAME", database["database"])


@pytest.fixture(scope="session")
def database():
    user = "user"
    password = "pass"
    database = "lendo"

    current_dir = Path(__file__).parent.parent
    print(current_dir)
    postgres_container = PostgresContainer(
        user=user, password=password, dbname=database
    ).with_volume_mapping(host=f"{current_dir}/db_init/", container="/docker-entrypoint-initdb.d/")
    try:
        postgres_container.start()
        yield {
            "username": user,
            "password": password,
            "database": database,
            "host": postgres_container.get_container_host_ip(),
            "port": postgres_container.get_exposed_port(5432),
            "connection_url": postgres_container.get_connection_url(),
        }

        postgres_container.stop()
    except Exception as e:
        print(e)
        raise e
    finally:
        try:
            postgres_container.stop()
        except Exception:
            pass


@pytest.fixture(scope="function")
async def db_connection(database):
    yield database
    db = await get_db()

    # This can be done better than run queries to clean up,
    # Refactor later
    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    db.execute("TRUNCATE TABLE applications")
    db.execute("SET FOREIGN_KEY_CHECKS = 1")
