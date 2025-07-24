from fastapi import APIRouter, HTTPException
from ..schemas import QueryRequest, QueryResponse
from ..config import settings

try:
    from pyadomd import Pyadomd
except Exception:  # fallback if pyadomd is unavailable or fails to load
    Pyadomd = None

router = APIRouter(prefix="/query", tags=["query"])

@router.post("", response_model=QueryResponse)
def run_query(req: QueryRequest):
    if Pyadomd is None:
        raise HTTPException(status_code=500, detail="pyadomd not installed")
    conn_str = settings.adomd_connection
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")
    with Pyadomd(conn_str) as conn:
        with conn.cursor().execute(req.mdx) as cur:
            columns = [c.caption for c in cur.getSchemaTable()]
            data = [dict(zip(columns, row)) for row in cur.fetchall()]
    return QueryResponse(columns=columns, data=data)
