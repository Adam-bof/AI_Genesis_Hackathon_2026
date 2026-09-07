"""
Python/C AST parser module
"""

from typing import List, Dict, Any
import ast as python_ast
try:
    import pycparser
    PYCCPARSER_AVAILABLE = True
except ImportError:
    PYCCPARSER_AVAILABLE = False


def parse_python(code: str) -> python_ast.AST:
    """Parse Python code using built-in ast module."""
    try:
        return python_ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")


def extract_functions(node: python_ast.AST) -> List[Dict]:
    """Extract all function definitions from AST."""
    functions = []
    
    for child in python_ast.walk(node):
        if isinstance(child, python_ast.FunctionDef):
            functions.append({
                "name": child.name,
                "lineno": child.lineno,
                "end_lineno": child.end_lineno,
                "args": [a.arg for a in child.args.args],
                "decorators": [d.id if hasattr(d, 'id') else str(d) for d in child.decorator_list] if hasattr(child, 'decorator_list') else [],
            })
    
    return functions


def extract_classes(node: python_ast.AST) -> List[Dict]:
    """Extract all class definitions from AST."""
    classes = []
    
    for child in python_ast.walk(node):
        if isinstance(child, python_ast.ClassDef):
            classes.append({
                "name": child.name,
                "lineno": child.lineno,
                "end_lineno": child.end_lineno,
                "methods": [m.name for m in child.body if isinstance(m, python_ast.FunctionDef)],
            })
    
    return classes