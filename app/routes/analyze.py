import os
from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
from app.models.schemas import AnalyzeResponse
from app.services.analyzer import analyze_code
from app.services.visualizer import generate_graphs

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("/")
async def analyze(files: List[UploadFile] = File(...)):
    file_paths = []
    os.makedirs("temp", exist_ok=True)

    # Saving of temp files (that uploaded)
    for file in files:
        temp_path = f"temp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(temp_path)

    # AST analysis
    analysis_result = analyze_code(file_paths)

    # Create graphs from results
    graph_paths = generate_graphs(analysis_result)

    # Return links to the result files
    return AnalyzeResponse(message="Analysis complete.", graphs=graph_paths)
