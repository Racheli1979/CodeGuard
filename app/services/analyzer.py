import ast
from typing import List, Dict


def analyze_code(file_paths: List[str]) -> Dict[str, dict]:
    """
    Checking every file, encryption it with AST, and return the information to analyze.
    """
    analysis_result = {}

    for path in file_paths:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            source_code = content.decode('utf-8')
        tree = {}
        try:
            tree = ast.parse(source_code)
        except Exception as e:
            print("Error parsing source code:", e)
        file_data = {
            "functions": [],
            "lines": len(source_code.splitlines())
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                start_line = node.lineno
                end_line = max(getattr(node.body[-1], "lineno", start_line), start_line)
                length = end_line - start_line + 1

                docstring = ast.get_docstring(node)
                file_data["functions"].append({
                    "name": node.name,
                    "length": length,
                    "docstring": bool(docstring),
                    "variables": get_assigned_variables(node),
                    "used_variables": get_used_variables(node)
                })

            analysis_result[path] = file_data

    return analysis_result


def get_assigned_variables(node: ast.FunctionDef) -> List[str]:
    """
    Return the assigned but not used variables.
    """
    variables = []
    for n in ast.walk(node):
        if isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Name):
                    variables.append(target.id)
    return variables


def get_used_variables(node: ast.FunctionDef) -> List[str]:
    """
    Return the used variables.
    """
    used = []
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            used.append(n.id)
    return used
