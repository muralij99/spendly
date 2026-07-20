import pytest
import database.db as db_module
from app import app
from database.db import init_db


@pytest.fixture
def client(monkeypatch, tmp_path):
    test_db = tmp_path / "test_spendly.db"
    monkeypatch.setattr(db_module, "DB_PATH", str(test_db))
    app.config["TESTING"] = True
    app.secret_key = "test-secret"
    init_db()
    with app.test_client() as client:
        yield client
