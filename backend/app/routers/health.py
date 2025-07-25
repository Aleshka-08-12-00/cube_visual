from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    from pyadomd import Pyadomd
except Exception:
    Pyadomd = None

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    """Simple health check ensuring connection to the cube works."""
    if Pyadomd is None:
        raise HTTPException(status_code=500, detail="pyadomd not installed")
    conn_str = settings.adomd_connection
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")
    try:
        with Pyadomd(conn_str) as conn:
            cur = conn.cursor()
            cur.execute("SELECT TABLE_CATALOG FROM $system.dbschema_catalogs")
            cur.fetchone()
            cur.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
    return {"status": "ok"}

