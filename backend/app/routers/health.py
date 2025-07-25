from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    import pyodbc
except Exception:
    pyodbc = None

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    """Simple health check ensuring connection to the cube works."""
    if pyodbc is None:
        raise HTTPException(status_code=500, detail="pyodbc not installed")
    conn_str = settings.adomd_connection
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")
    try:
        with pyodbc.connect(conn_str) as conn:
            cur = conn.cursor()
            cur.execute("SELECT TABLE_CATALOG FROM $system.dbschema_catalogs")
            cur.fetchone()
            cur.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
    return {"status": "ok"}

