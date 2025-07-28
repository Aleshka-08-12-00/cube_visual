import os
import sys
from typing import Any, Dict, List, Tuple
from decimal import Decimal
from .config import settings

def _ensure_dll():
    p = settings.adomd_dll_path
    if p and os.path.isfile(p):
        os.add_dll_directory(os.path.dirname(p))
        sys.path.append(os.path.dirname(p))

_ensure_dll()
from pyadomd import Pyadomd

def fetch(query: str) -> Tuple[List[str], List[List[Any]]]:
    with Pyadomd(settings.adomd_connection) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = []
            for record in cur.fetchall():
                row = []
                for value in record:
                    if isinstance(value, Decimal):
                        # Convert Decimals to float for JSON serialization
                        row.append(float(value))
                    else:
                        row.append(value)
                rows.append(row)
            return cols, rows

def fetch_limited(query: str, limit: int) -> Tuple[List[str], List[List[Any]]]:
    cols, rows = fetch(query)
    if limit and limit > 0:
        rows = rows[:limit]
    return cols, rows
