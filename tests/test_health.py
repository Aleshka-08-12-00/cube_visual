from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routers import health


class DummyConn:
    def getDBSchemaCatalogs(self):
        return []


class DummyProvider:
    def connect(self, location, username=None, password=None):
        return DummyConn()


def test_health_success(monkeypatch):
    monkeypatch.setattr(health, "XMLAProvider", DummyProvider)
    monkeypatch.setattr(health.settings, "xmla_url", "localhost")
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_no_provider(monkeypatch):
    monkeypatch.setattr(health, "XMLAProvider", None)
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 500
    assert resp.json()["detail"] == "xmla library not installed"
