from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from ..adomd import fetch
from ..mdx_builder import build_mdx

DEFAULT_MDX = (
    "SELECT\n"
    "  NON EMPTY\n"
    "    [Время].[Год - Квартал - Месяц - День].&[2024].Children\n"
    "    * { [Measures].[реализация руб] }\n"
    "  ON COLUMNS,\n"
    "  NON EMPTY\n"
    "    [Товар].[Концерн].Members\n"
    "  ON ROWS\n"
    "FROM [NextGen]"
)

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
    if req.mdx:
        mdx = req.mdx
    elif req.cube:
        mdx = build_mdx(req.cube, req.measures, req.rows, req.columns, req.slicers)
    else:
        mdx = DEFAULT_MDX
    cols, rows = fetch(mdx)
    return {"mdx": mdx, "columns": cols, "rows": rows}

@router.get("/health")
def health():
    cols, rows = fetch("SELECT TABLE_CATALOG FROM $SYSTEM.DBSCHEMA_CATALOGS")
    return {"status": "ok"}
