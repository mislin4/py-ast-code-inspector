import ast
from typing import Set, List, Dict, Any


class CodeSyntaxInspector(ast.NodeVisitor):
    """
    Python kod dizgilerini AST düzeyinde analiz ederek
    tanımsız kütüphane çağrılarını ve eksik bağımlılıkları raporlar.
    """

    def __init__(self):
        self.imported_modules: Set[str] = set()
        self.defined_functions: Set[str] = set()
        self.called_functions: List[str] = []
        self.accessed_attributes: List[Dict[str, Any]] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imported_modules.add(alias.name)
            if alias.asname:
                self.imported_modules.add(alias.asname)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imported_modules.add(node.module)
        for alias in node.names:
            self.imported_modules.add(alias.name)
            if alias.asname:
                self.imported_modules.add(alias.asname)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.called_functions.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                self.accessed_attributes.append({
                    "object": node.func.value.id,
                    "attribute": node.func.attr,
                    "lineno": node.lineno,
                })
        self.generic_visit(node)


def inspect_source(source_code: str) -> Dict[str, Any]:
    """
    Verilen Python kaynak kodunu parse eder ve özet sözdizim tablosu döner.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as err:
        return {
            "valid_syntax": False,
            "error": f"SyntaxError at line {err.lineno}: {err.msg}",
            "tree": None,
        }

    inspector = CodeSyntaxInspector()
    inspector.visit(tree)

    return {
        "valid_syntax": True,
        "imports": sorted(list(inspector.imported_modules)),
        "functions_defined": sorted(list(inspector.defined_functions)),
        "calls": inspector.called_functions,
        "attribute_calls": inspector.accessed_attributes,
    }
