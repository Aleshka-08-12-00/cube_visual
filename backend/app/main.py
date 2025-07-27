from fastapi import FastAPI

from .routers import query, reports, fields, health
from .connection import open_connection, close_connection

app = FastAPI(title="Cube Visual")


@app.on_event("startup")
def _startup() -> None:
    """Establish the cube connection on startup."""
    try:
        open_connection()
    except Exception:
        # connection errors will surface when endpoints are called
        pass


@app.on_event("shutdown")
def _shutdown() -> None:
    close_connection()

app.include_router(query.router)
app.include_router(reports.router)
app.include_router(fields.router)
app.include_router(health.router)
