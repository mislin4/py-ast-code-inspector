# py-ast-code-inspector

A lightweight static analysis and runtime traceback triage utility designed for Python scripts executed within automated analytical pipelines.

## Overview
Dynamic code execution environments require fast, non-intrusive validation before and after running generated scripts. `py-ast-code-inspector` provides two decoupled layers:
1. **Static AST Inspection:** Parses Python source code using the abstract syntax tree (`ast`) to extract imports, function definitions, and attribute accesses without executing the code.
2. **Traceback Triage:** Parses execution error logs (`stderr`) to reliably extract runtime exception types (`KeyError`, `NameError`, `AttributeError`), offending line numbers, and target symbols.

## Installation & Tests

```bash
git clone [https://github.com/mislin4/py-ast-code-inspector.git](https://github.com/mislin4/py-ast-code-inspector.git)
cd py-ast-code-inspector
pip install -r requirements.txt
pytest tests/ -v
