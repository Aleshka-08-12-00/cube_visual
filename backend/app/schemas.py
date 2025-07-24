from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    mdx: str

class QueryResponse(BaseModel):
    columns: List[str]
    data: List[Dict[str, Any]]

class Report(BaseModel):
    name: str
    mdx: str
