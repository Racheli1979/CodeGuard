import os
import shutil
from fastapi import UploadFile
from typing import List

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """
    Save the files in temp directory and return the paths to files.
    """
    file_paths = []
    for file in files:
        temp_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(temp_path)
    return file_paths


def delete_temp_files(file_paths: List[str]):
    """
    Delete temp files after using.
    """
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)
