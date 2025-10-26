import matplotlib.pyplot as plt
import os
from typing import Dict
from collections import Counter

OUTPUT_DIR = "static/graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_graphs(analysis_result: Dict[str, dict]) -> Dict[str, str]:
    """
    Create graphs from analysis results, save as PNG files, and return the paths.
    """
    graph_paths = {}
    path1 = hist_by_func_length(analysis_result)
    graph_paths["function_histogram"] = path1

    path2 = pai_by_issue_types(analysis_result)
    graph_paths["issue_pie_chart"] = path2

    path3 = bar_graph_by_file(analysis_result)
    graph_paths["issues_bar_chart"] = path3

    return graph_paths


def hist_by_func_length(analysis_result: Dict[str, dict]):
    # פונקציה 1: היסטוגרמה של אורכי פונקציות
    func_lengths = [
        func["length"]
        for file_data in analysis_result.values()
        for func in file_data["functions"]
    ]
    plt.figure()
    plt.hist(func_lengths, bins=10, color='skyblue')
    plt.title("Function Length Distribution")
    plt.xlabel("Lines")
    plt.ylabel("Number of Functions")
    path1 = os.path.join(OUTPUT_DIR, "function_lengths.png")
    plt.savefig(path1)
    return path1

def pai_by_issue_types(analysis_result: Dict[str, dict]):
    # פונקציה 2: פאי לפי סוג בעיות
    issue_types = []
    for file_data in analysis_result.values():
        if file_data["lines"] > 200:
            issue_types.append("File too long")
        for func in file_data["functions"]:
            if func["length"] > 20:
                issue_types.append("Function too long")
            if not func["docstring"]:
                issue_types.append("Missing docstring")
            unused = set(func["variables"]) - set(func["used_variables"])
            if unused:
                issue_types.append("Unused variables")

    counts = Counter(issue_types)
    plt.figure()
    plt.pie(counts.values(), labels=counts, autopct='%1.1f%%',colors=("magenta","yellow","green"))
    plt.title("Issue Types Distribution")
    path2 = os.path.join(OUTPUT_DIR, "issues_pie.png")
    plt.savefig(path2)
    return path2

def bar_graph_by_file(analysis_result):
    # פונקציה 3: גרף עמודות לפי קובץ
    file_issues = {}
    for file_path, file_data in analysis_result.items():
        count = 0
        if file_data["lines"] > 200:
            count += 1
        for func in file_data["functions"]:
            if func["length"] > 20:
                count += 1
            if not func["docstring"]:
                count += 1
            unused = set(func["variables"]) - set(func["used_variables"])
            if unused:
                count += 1
        file_issues[os.path.basename(file_path)] = count

    plt.figure()
    plt.bar(file_issues.keys(), file_issues.values(), color='orange')
    plt.title("Issues per File")
    plt.xlabel("File")
    plt.ylabel("Number of Issues")
    path3 = os.path.join(OUTPUT_DIR, "file_issues_bar.png")
    plt.savefig(path3)
    return path3