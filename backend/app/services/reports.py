import json
import os
from typing import List
from ..schemas import Report

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'reports.json')
DATA_FILE = os.path.normpath(DATA_FILE)


def load_reports() -> List[Report]:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            return [Report(**r) for r in data]
    return []


def save_reports(reports: List[Report]):
    with open(DATA_FILE, 'w') as f:
        json.dump([r.dict() for r in reports], f)


def add_report(report: Report):
    reports = load_reports()
    reports.append(report)
    save_reports(reports)
