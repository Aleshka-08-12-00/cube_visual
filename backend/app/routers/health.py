from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    from olap.xmla.xmla import XMLAProvider
except Exception:
    XMLAProvider = None

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    """Simple health check ensuring connection to the cube works."""
    if XMLAProvider is None:
        raise HTTPException(status_code=500, detail="xmla library not installed")

    if not settings.xmla_url:
        raise HTTPException(status_code=500, detail="XMLA_URL not configured")

    try:
        provider = XMLAProvider()
        conn = provider.connect(
            location=settings.xmla_url,
            username=settings.xmla_username or None,
            password=settings.xmla_password or None,
        )
        conn.getDBSchemaCatalogs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}")
    return {"status": "ok"}

