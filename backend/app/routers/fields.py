from fastapi import APIRouter, HTTPException
from ..connection import open_connection

router = APIRouter(prefix="/fields", tags=["fields"])


@router.get("")
def list_fields():
    try:
        conn = open_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT DIMENSION_NAME FROM $SYSTEM.MDSCHEMA_DIMENSIONS")
            dimensions = [row[0] for row in cur.fetchall()]

        with conn.cursor() as cur:
            cur.execute("SELECT MEASURE_NAME FROM $SYSTEM.MDSCHEMA_MEASURES")
            measures = [row[0] for row in cur.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"dimensions": dimensions, "measures": measures}
