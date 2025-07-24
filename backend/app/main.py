from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import json
import os

try:
    from pyadomd import Pyadomd
except ImportError:  # fallback for environments without pyadomd
    Pyadomd = None

app = FastAPI(title="Cube Visual")

DATA_FILE = os.path.join(os.path.dirname(__file__), 'reports.json')

def load_reports() -> List[Dict]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reports(reports: List[Dict]):
    with open(DATA_FILE, 'w') as f:
        json.dump(reports, f)

class QueryRequest(BaseModel):
    mdx: str

class SaveReportRequest(BaseModel):
    name: str
    mdx: str

@app.post('/query')
def run_query(req: QueryRequest):
    if Pyadomd is None:
        raise HTTPException(status_code=500, detail="pyadomd not installed")
    conn_str = os.getenv('ADOMD_CONNECTION')
    if not conn_str:
        raise HTTPException(status_code=500, detail="ADOMD_CONNECTION not configured")
    with Pyadomd(conn_str) as conn:
        with conn.cursor().execute(req.mdx) as cur:
            columns = [c.caption for c in cur.getSchemaTable()]
            data = [dict(zip(columns, row)) for row in cur.fetchall()]
    return {"columns": columns, "data": data}

@app.get('/reports')
def get_reports():
    return load_reports()

@app.post('/reports')
def save_report(req: SaveReportRequest):
    reports = load_reports()
    reports.append({"name": req.name, "mdx": req.mdx})
    save_reports(reports)
    return {"status": "saved"}
