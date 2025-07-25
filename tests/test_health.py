from fastapi.testclient import TestClient
from backend.app.main import app
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

    def __enter__(self):
        return DummyConn()

    def __exit__(self, exc_type, exc, tb):
        pass


def test_health_success(monkeypatch):
    monkeypatch.setattr(health, "Pyadomd", DummyPyadomd)
    monkeypatch.setattr(health, "clr", object())
    monkeypatch.setattr(health.settings, "adomd_conn_str", "cs")
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_no_provider(monkeypatch):
    monkeypatch.setattr(health, "Pyadomd", None)
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 500
    assert resp.json()["detail"] == "pyadomd library not installed"
