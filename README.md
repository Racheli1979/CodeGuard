# 🧠 CodeGuard – Code Analysis System

Welcome to **CodeGuard**, a backend system for analyzing Python code quality as part of a simulated CI/CD process using a `wit push` command.

---

## 🚀 Project Overview

CodeGuard is a FastAPI-based server that:

- Analyzes Python files using the AST module
- Detects common code quality issues
- Generates visual insights using matplotlib

It simulates a minimal Continuous Integration (CI) system focused on code correctness and maintainability.

---

## 🧰 Technologies Used

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **AST Analysis**: `ast`
- **Graphs**: `matplotlib`
- **API Docs**: Swagger UI (`/docs`)

---

## 🗂 Folder Structure

```
codeguard-backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── routes/              # API endpoints
│   │   ├── analyze.py
│   │   └── alerts.py
│   ├── services/            # Core logic (AST, analysis, visualization)
│   │   ├── analyzer.py
│   │   ├── issues.py
│   │   └── visualizer.py
│   ├── utils/
│   │   └── file_handler.py
│   └── models/
│       └── schemas.py
├── static/graphs/           # Output PNG graphs
├── temp/                    # Temporary uploaded files
├── tests/                   # Unit and integration tests
├── requirements.txt
└── README.md
```

---

## 🧪 Code Quality Checks

Each Python file is analyzed for the following:

| Check                                | Description                                                    |
|--------------------------------------|----------------------------------------------------------------|
| ✅ Function Length                    | Warns if a function is longer than 20 lines                    |
| ✅ File Length                        | Warns if a file exceeds 200 lines                              |
| ✅ Unused Variables                   | Warns if a variable is assigned but not used                   |
| ✅ Missing Docstrings                 | Warns if a function has no docstring                           |
| 🌍 Bonus: Non-English Variable Names | Warns if variable names use non-English (e.g., Hebrew) letters |

---

## 📊 Generated Graphs

When calling `/analyze`, the system returns:

1. 📈 **Histogram** – Function lengths
2. 🥧 **Pie Chart** – Issue type distribution
3. 📊 **Bar Chart** – Issues per file

---

## 🌐 API Endpoints

### POST `/analyze`

**Description**: Upload one or more `.py` files and get back graph images.

**Response**:

```json
{
  "message": "Analysis complete.",
  "graphs": {
    "function_histogram": "static/graphs/function_lengths.png",
    "issue_pie_chart": "static/graphs/issues_pie.png",
    "issues_bar_chart": "static/graphs/file_issues_bar.png"
  }
}
```

---

### POST `/alerts`

**Description**: Upload `.py` files and receive a list of detected issues.

**Response**:

```json
{
  "message": "Issues detected.",
  "issues": [
    {
      "file": "main.py",
      "type": "FunctionLength",
      "message": "Function 'calculate' exceeds 20 lines."
    }
  ]
}
```

---

## 🛠 Installation & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/HadassaAvimorNew/codeguard-backend.git
   cd codeguard-backend
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Visit the docs**\
   Open your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📌 License

This project is for educational use only as part of a backend development final project.

---

## 👤 Author

GitHub: [Racheli1979](https://github.com/Racheli1979)

