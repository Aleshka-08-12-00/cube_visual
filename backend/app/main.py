from fastapi import FastAPI

from .routers import query, reports, fields

app = FastAPI(title="Cube Visual")

app.include_router(query.router)
app.include_router(reports.router)
app.include_router(fields.router)
