from pydantic import BaseModel
from typing import List, Optional


class Issue(BaseModel):
    file: str
    line: Optional[int] = None
    type: str
    message: str


class AnalyzeResponse(BaseModel):
    message: str
    graphs: dict


class AlertsResponse(BaseModel):
    message: str
    issues: List[Issue]
