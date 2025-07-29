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
    """dimensions endpoint should deduplicate dimension rows."""
    # Mock data for hierarchies
    hier_cols = [
        "DIMENSION_UNIQUE_NAME",
        "HIERARCHY_UNIQUE_NAME",
        "DIMENSION_TYPE",
        "IS_VIRTUAL",
    ]
    hier_rows = [
        ["[Sales]", "[Sales].[H1]", 1, False],
        ["[Sales]", "[Sales].[H2]", 1, False],
        ["[Products]", "[Products].[H1]", 1, False],
    ]

    # Mock data for dimensions metadata
    dim_cols = [
        "DIMENSION_UNIQUE_NAME",
        "DIMENSION_NAME",
        "DIMENSION_CAPTION",
        "DIMENSION_IS_VISIBLE",
    ]
    dim_rows = [
        ["[Sales]", "Sales", "Sales", True],
        ["[Products]", "Products", "Products", True],
    ]

    def fake_fetch_limited(query: str, limit: int):
        if "MDSCHEMA_HIERARCHIES" in query:
            return hier_cols, hier_rows
        if "MDSCHEMA_DIMENSIONS" in query:
            return dim_cols, dim_rows
        return [], []

    monkeypatch.setattr("app.routers.schema.fetch_limited", fake_fetch_limited)
    resp = client.get("/schema/dimensions", params={"cube": "NextGen"})
    assert resp.status_code == 200
    data = resp.json()
    # Should return only unique dimensions
    assert data == [
        {"dimension_name": "Sales", "dimension_unique_name": "[Sales]"},
        {"dimension_name": "Products", "dimension_unique_name": "[Products]"},
    ]
