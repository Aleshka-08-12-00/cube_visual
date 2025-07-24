from fastapi import APIRouter
from typing import List
from ..schemas import Report
from ..services import reports as reports_service

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("", response_model=List[Report])
def list_reports():
    return reports_service.load_reports()

@router.post("", response_model=dict)
def create_report(report: Report):
    reports_service.add_report(report)
    return {"status": "saved"}
