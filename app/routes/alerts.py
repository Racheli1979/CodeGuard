import os
from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
from app.models.schemas import AlertsResponse
from app.services.analyzer import analyze_code
from app.services.issues import detect_issues

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/")
async def alerts(files: List[UploadFile] = File(...)):
    file_paths = []
    os.makedirs("temp", exist_ok=True)

    for file in files:
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(temp_path)

    # AST analysis
    analysis_result = analyze_code(file_paths)

    # problem detection
    issues = detect_issues(analysis_result)
    response = AlertsResponse(message="Issues detected.", issues=issues)

    return response
