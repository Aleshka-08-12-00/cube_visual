from fastapi import APIRouter, HTTPException
from ..schemas import QueryRequest, QueryResponse
from ..connection import open_connection

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def run_query(req: QueryRequest):
    try:
        conn = open_connection()
        with conn.cursor() as cur:
            cur.execute(req.mdx)
            columns = [d[0] for d in cur.description]
            rows = cur.fetchall()
        data = [dict(zip(columns, r)) for r in rows]
        return QueryResponse(columns=columns, data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
