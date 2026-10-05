import pytest
from inspector import inspect_source, TracebackTriage


def test_ast_inspector_detects_imports_and_calls():
    code = (
        "import numpy as np\n"
        "import pandas as pd\n"
        "\n"
        "def compute_mean(data):\n"
        "    return np.mean(data)\n"
    )
    analysis = inspect_source(code)
    assert analysis["valid_syntax"] is True
    assert "numpy" in analysis["imports"]
    assert "pandas" in analysis["imports"]
    assert "compute_mean" in analysis["functions_defined"]


def test_ast_inspector_handles_syntax_error():
    bad_code = "def broken_syntax(:\n    pass"
    analysis = inspect_source(bad_code)
    assert analysis["valid_syntax"] is False
    assert "SyntaxError" in analysis["error"]


def test_traceback_triage_keyerror():
    mock_stderr = (
        "Traceback (most recent call last):\n"
        "  File 'script.py', line 12, in <module>\n"
        "    val = df['non_existing_col']\n"
        "KeyError: 'non_existing_col'\n"
    )
    diagnostic = TracebackTriage.parse(mock_stderr)
    assert diagnostic.error_type == "KeyError"
    assert diagnostic.failed_line_number == 12
    assert diagnostic.target_symbol == "non_existing_col"


def test_traceback_triage_nameerror():
    mock_stderr = (
        "Traceback (most recent call last):\n"
        "  File 'process.py', line 5, in <module>\n"
        "    result = plt.show()\n"
        "NameError: name 'plt' is not defined\n"
    )
    diagnostic = TracebackTriage.parse(mock_stderr)
    assert diagnostic.error_type == "NameError"
    assert diagnostic.failed_line_number == 5
    assert diagnostic.target_symbol == "plt"
