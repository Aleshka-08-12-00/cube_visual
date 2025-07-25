from fastapi import APIRouter, HTTPException
from ..config import settings
import os

try:
    import clr  # type: ignore
    from System.Reflection import Assembly  # type: ignore
    from pyadomd import Pyadomd  # type: ignore
except Exception:  # pragma: no cover - import errors
    clr = None
    Assembly = None
    Pyadomd = None

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    """Simple health check ensuring connection to the cube works."""
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
                cur.execute("SELECT CATALOG_NAME FROM $SYSTEM.MDSCHEMA_CUBES")
                cur.fetchone()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
    return {"status": "ok"}

