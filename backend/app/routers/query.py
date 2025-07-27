from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from ..adomd import fetch
from ..mdx_builder import build_mdx

router = APIRouter(prefix="/query", tags=["query"])

class RunRequest(BaseModel):
    mdx: Optional[str] = None
    cube: Optional[str] = None
    measures: List[str] = Field(default_factory=list)
    rows: List[str] = Field(default_factory=list)
    columns: List[str] = Field(default_factory=list)
    slicers: List[str] = Field(default_factory=list)

@router.post("/run")
def run(req: RunRequest):
    mdx = req.mdx or build_mdx(req.cube or "", req.measures, req.rows, req.columns, req.slicers)
    cols, rows = fetch(mdx)
    return {"mdx": mdx, "columns": cols, "rows": rows}

@router.get("/health")
def health():
    cols, rows = fetch("SELECT TABLE_CATALOG FROM $SYSTEM.DBSCHEMA_CATALOGS")
    return {"status": "ok"}
