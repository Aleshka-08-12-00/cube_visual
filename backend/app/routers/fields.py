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

router = APIRouter(prefix="/fields", tags=["fields"])

@router.get("")
def list_fields():
    if Pyadomd is None or clr is None:
        return {"dimensions": [], "measures": []}

    if not settings.adomd_conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONN_STR not configured")

    try:
        if settings.adomd_dll_path:
            os.add_dll_directory(os.path.dirname(settings.adomd_dll_path))
            Assembly.LoadFrom(settings.adomd_dll_path)

        with Pyadomd(settings.adomd_conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DIMENSION_NAME FROM $SYSTEM.MDSCHEMA_DIMENSIONS")
                dimensions = [row[0] for row in cur.fetchall()]

        with Pyadomd(settings.adomd_conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MEASURE_NAME FROM $SYSTEM.MDSCHEMA_MEASURES")
                measures = [row[0] for row in cur.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"dimensions": dimensions, "measures": measures}
