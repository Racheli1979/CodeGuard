import re
from typing import Dict, List
from app.models.schemas import Issue

HEBREW_PATTERN = re.compile(r"[\u0590-\u05FF]")  # טווח יוניקוד לאותיות בעברית


def detect_issues(analysis_result: Dict[str, dict]) -> List[Issue]:
    """
    Accept the analysis results and return list of issues in this format:
    [
        {"file": ..., "line": ..., "type": ..., "message": ...}
    ]
    """
    issues: List[Issue] = []

    for file_path, file_data in analysis_result.items():
        if file_data["lines"] > 200:
            issues.append(Issue(file=file_path, line=None, type="FileLength",
                                message="File exceeds 200 lines."))

        for func in file_data["functions"]:
            if func["length"] > 20:
                issues.append(Issue(file=file_path, line=None, type="FunctionLength",
                                    message=f"Function '{func['name']}' exceeds 20 lines."))

            if not func["docstring"]:
                issues.append(Issue(file=file_path, line=None, type="MissingDocstring",
                                    message=f"Function '{func['name']}' has no docstring."))

            # unused variables
            unused_vars = set(func["variables"]) - set(func["used_variables"])
            for var in unused_vars:
                issues.append(Issue(file=file_path, line=None, type="UnusedVariable",
                                    message=f"Variable '{var}' is assigned but never used."))

            # Variables in hebrew
            for var in func["variables"]:
                if HEBREW_PATTERN.search(var):
                    issues.append(Issue(file=file_path, line=None, type="NonEnglishVariable",
                                        message=f"Variable '{var}' is not in English."))

    return issues
