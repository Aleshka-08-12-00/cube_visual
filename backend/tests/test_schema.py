import os
import sys
from pathlib import Path
import types

import pytest
from fastapi.testclient import TestClient

# Allow importing from the backend package
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Stub pyadomd to avoid requiring a .NET runtime during tests
sys.modules.setdefault("pyadomd", types.ModuleType("pyadomd")).Pyadomd = object

from app.main import app

# We'll monkeypatch fetch_limited to avoid external dependencies

@pytest.fixture
def client():
    return TestClient(app)

def test_dimensions_deduplication(monkeypatch, client):
    # Prepare mocked data with duplicate dimension rows
    sample_cols = ["DIMENSION_NAME", "DIMENSION_UNIQUE_NAME"]
    sample_rows = [
        ["Sales", "[Sales]"],
        ["Sales", "[Sales]"],
        ["Products", "[Products]"]
    ]

    def fake_fetch_limited(query: str, limit: int):
        return sample_cols, sample_rows

    monkeypatch.setattr("app.routers.schema.fetch_limited", fake_fetch_limited)
    resp = client.get("/schema/dimensions", params={"cube": "NextGen"})
    assert resp.status_code == 200
    data = resp.json()
    # Should return only unique dimensions
    assert data == [
        {"dimension_name": "Sales", "dimension_unique_name": "[Sales]"},
        {"dimension_name": "Products", "dimension_unique_name": "[Products]"}
    ]

