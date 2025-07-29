import os
import sys
from pathlib import Path
import types

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Stub pyadomd to avoid requiring .NET runtime during tests
sys.modules.setdefault("pyadomd", types.ModuleType("pyadomd")).Pyadomd = object

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)


def test_strip_total_row(monkeypatch, client):
    cols = ["name", "value"]
    rows = [["All", 30], ["A", 10], ["B", 20]]

    def fake_fetch(mdx: str):
        return cols, rows

    monkeypatch.setattr("app.routers.query.fetch", fake_fetch)
    resp = client.post("/query/run", json={"mdx": "SELECT"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["rows"] == [["A", 10], ["B", 20]]
