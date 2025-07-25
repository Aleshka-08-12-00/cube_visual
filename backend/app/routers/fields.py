from fastapi import APIRouter, HTTPException
from ..config import settings

try:
    from olap.xmla.xmla import XMLAProvider
except Exception:
    XMLAProvider = None

router = APIRouter(prefix="/fields", tags=["fields"])

@router.get("")
def list_fields():
    if XMLAProvider is None:
        return {"dimensions": [], "measures": []}

    if not settings.xmla_url:
        raise HTTPException(status_code=500, detail="XMLA_URL not configured")

    try:
        provider = XMLAProvider()
        conn = provider.connect(
            location=settings.xmla_url,
            username=settings.xmla_username or None,
            password=settings.xmla_password or None,
        )
        dims = conn.getMDSchemaDimensions(Catalog=settings.xmla_catalog or None)
        dimensions = [d.DIMENSION_NAME for d in dims]
        meas = conn.getMDSchemaMeasures(Catalog=settings.xmla_catalog or None)
        measures = [m.MEASURE_NAME for m in meas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"dimensions": dimensions, "measures": measures}
