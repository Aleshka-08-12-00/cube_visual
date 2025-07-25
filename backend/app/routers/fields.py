from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    import pyodbc
except Exception:
    pyodbc = None

router = APIRouter(prefix="/fields", tags=["fields"])

@router.get("")
def list_fields():
    if pyodbc is None:
        # Fallback with empty lists when pyodbc is not available
        return {"dimensions": [], "measures": []}

    conn_str = settings.adomd_connection
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")

    try:
        with pyodbc.connect(conn_str) as conn:
            cur = conn.cursor()
            # List dimensions
            cur.execute("SELECT DIMENSION_NAME FROM $system.MDSCHEMA_DIMENSIONS")
            dimensions = [row[0] for row in cur.fetchall()]
            # List measures
            cur.execute("SELECT MEASURE_NAME FROM $system.MDSCHEMA_MEASURES")
            measures = [row[0] for row in cur.fetchall()]
            cur.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"dimensions": dimensions, "measures": measures}
