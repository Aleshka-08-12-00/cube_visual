from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    from pyadomd import Pyadomd
except Exception:
    Pyadomd = None

router = APIRouter(prefix="/fields", tags=["fields"])

@router.get("")
def list_fields():
    if Pyadomd is None:
        # Fallback with empty lists when pyadomd is not available
        return {"dimensions": [], "measures": []}

    conn_str = settings.adomd_connection
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")

    try:
        with Pyadomd(conn_str) as conn:
            # List dimensions
            with conn.cursor().execute("SELECT DIMENSION_NAME FROM $system.MDSCHEMA_DIMENSIONS") as cur:
                dimensions = [row[0] for row in cur.fetchall()]
            # List measures
            with conn.cursor().execute("SELECT MEASURE_NAME FROM $system.MDSCHEMA_MEASURES") as cur:
                measures = [row[0] for row in cur.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"dimensions": dimensions, "measures": measures}
