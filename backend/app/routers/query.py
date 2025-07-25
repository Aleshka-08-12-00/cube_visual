from fastapi import APIRouter, HTTPException
from ..schemas import QueryRequest, QueryResponse
from ..config import settings

try:
    from olap.xmla.xmla import XMLAProvider
except Exception:
    XMLAProvider = None

router = APIRouter(prefix="/query", tags=["query"])

@router.post("", response_model=QueryResponse)
def run_query(req: QueryRequest):
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
        result = conn.Execute(req.mdx, Catalog=settings.xmla_catalog or None)
        columns = [
            m.CAPTION if hasattr(m, "CAPTION") else m.getUniqueName()
            for m in result.getAxisTuple(0)
        ]
        rows = result.getAxisTuple(1)
        cells = result.getSlice(properties="Value")
        data = []
        if rows:
            for r_idx, row in enumerate(rows):
                row_caption = row.CAPTION if hasattr(row, "CAPTION") else row.getUniqueName()
                row_values = cells[r_idx]
                row_dict = {"Row": row_caption}
                for c_idx, col in enumerate(columns):
                    row_dict[col] = row_values[c_idx]
                data.append(row_dict)
            columns = ["Row"] + columns
        else:
            row_dict = {}
            for c_idx, col in enumerate(columns):
                row_dict[col] = cells[c_idx]
            data.append(row_dict)

        return QueryResponse(columns=columns, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
