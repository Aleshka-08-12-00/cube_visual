from fastapi import FastAPI

from .routers import query, reports

app = FastAPI(title="Cube Visual")

app.include_router(query.router)
app.include_router(reports.router)
