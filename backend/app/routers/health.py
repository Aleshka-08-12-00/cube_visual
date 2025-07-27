from fastapi import APIRouter, HTTPException
from ..connection import open_connection

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    """Simple health check ensuring connection to the cube works."""
    try:
        conn = open_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT CATALOG_NAME FROM $SYSTEM.MDSCHEMA_CUBES")
            cur.fetchone()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
    return {"status": "ok"}

