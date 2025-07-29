from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from ..adomd import fetch
from ..mdx_builder import build_mdx


def _to_float(v: Any) -> float | None:
    """Convert values to ``float`` if possible."""
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", "."))
    except Exception:
        return None


def _strip_total_row(columns: List[str], rows: List[List[Any]]) -> List[List[Any]]:
    """Remove leading or trailing grand total row if present."""
    if len(rows) <= 1 or len(columns) <= 1:
        return rows

    num_cols = len(columns) - 1

    # Convert all numeric values to ``float`` and compute column totals.
    converted: list[list[float]] = []
    totals = [0.0] * num_cols
    for r in rows:
        if len(r) < len(columns):
            return rows
        vals = []
        for i in range(num_cols):
            val = _to_float(r[i + 1])
            if val is None:
                return rows
            vals.append(val)
            totals[i] += val
        converted.append(vals)

    def is_total(idx: int) -> bool:
        candidate = converted[idx]
        rest = [totals[i] - candidate[i] for i in range(num_cols)]
        return all(abs(candidate[i] - rest[i]) < 1e-6 for i in range(num_cols))

    if is_total(0):
        return rows[1:]
    if is_total(len(rows) - 1):
        return rows[:-1]
    return rows

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
    rows = _strip_total_row(cols, rows)
    return {"mdx": mdx, "columns": cols, "rows": rows}

@router.get("/health")
def health():
    cols, rows = fetch("SELECT TABLE_CATALOG FROM $SYSTEM.DBSCHEMA_CATALOGS")
    return {"status": "ok"}
