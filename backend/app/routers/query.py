from fastapi import APIRouter, HTTPException
import os
from ..schemas import QueryRequest, QueryResponse
from ..config import settings

try:
    import clr  # type: ignore
    from System.Reflection import Assembly  # type: ignore
    from pyadomd import Pyadomd  # type: ignore
except Exception:  # pragma: no cover - import errors
    clr = None
    Assembly = None
    Pyadomd = None

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def run_query(req: QueryRequest):
    if Pyadomd is None or clr is None:
        raise HTTPException(status_code=500, detail="pyadomd library not installed")

    if not settings.adomd_conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONN_STR not configured")

    try:
        if settings.adomd_dll_path:
            os.add_dll_directory(os.path.dirname(settings.adomd_dll_path))
            Assembly.LoadFrom(settings.adomd_dll_path)

        with Pyadomd(settings.adomd_conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(req.mdx)
                columns = [d[0] for d in cur.description]
                rows = cur.fetchall()
        data = [dict(zip(columns, r)) for r in rows]
        return QueryResponse(columns=columns, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
