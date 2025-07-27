from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import connection
from backend.app.routers import health


class DummyCursor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def execute(self, sql):
        pass

    def fetchone(self):
        return ["ok"]


class DummyConn:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def cursor(self):
        return DummyCursor()


class DummyPyadomd:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def open(self):
        pass

    def close(self):
        pass

    def cursor(self):
        return DummyCursor()


def test_health_success(monkeypatch):
    monkeypatch.setattr(connection, "Pyadomd", DummyPyadomd)
    monkeypatch.setattr(connection, "clr", object())
    monkeypatch.setattr(connection.settings, "adomd_conn_str", "cs")
    monkeypatch.setattr(connection.settings, "adomd_dll_path", "")
    connection._conn = None
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_no_provider(monkeypatch):
    monkeypatch.setattr(connection, "Pyadomd", None)
    connection._conn = None
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 500
    assert resp.json()["detail"] == "pyadomd library not installed"
