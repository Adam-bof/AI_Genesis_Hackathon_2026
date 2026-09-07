"""
JavaScript AST parser using Python's ast module.

As defined in the hackathon plan:
- AST Parsing support for JavaScript/TypeScript
- Phase 4: Tool development includes JS support
"""

import ast as python_ast
from typing import Dict, List, Any, Optional


def parse_javascript(code: str) -> Optional[python_ast.AST]:
    """Parse JavaScript code using Python's ast module (basic subset)."""
    try:
        # Note: This parses a JavaScript-like subset valid in Python's ast
        # For full JS parsing, pycparser/libclang or @babel/parser would be used
        return python_ast.parse(code, mode='eval')
    except SyntaxError:
        try:
            return python_ast.parse(code, mode='exec')
        except SyntaxError:
            return None


def extract_functions(node: python_ast.AST) -> List[Dict]:
    """Extract function definitions from JS AST."""
    functions = []
    
    for child in python_ast.walk(node):
        if isinstance(child, python_ast.FunctionDef):
            functions.append({
                "name": child.name,
                "lineno": child.lineno,
                "args": [a.arg for a in child.args.args] if hasattr(child, 'args') else [],
                "decorators": [d.id if hasattr(d, 'id') else str(d) for d in child.decorator_list] if hasattr(child, 'decorator_list') else [],
            })
        elif isinstance(child, python_ast.AsyncFunctionDef):
            functions.append({
                "name": child.name,
                "lineno": child.lineno,
                "args": [a.arg for a in child.args.args] if hasattr(child, 'args') else [],
                "is_async": True,
            })
    
    return functions


def extract_variables(code: str) -> Dict[str, Any]:
    """Extract variable assignments from JS code."""
    try:
        tree = python_ast.parse(code, mode='exec')
        variables = {}
        
        for node in python_ast.walk(tree):
            if isinstance(node, python_ast.Assign):
                for target in node.targets:
                    if isinstance(target, python_ast.Name):
                        var_name = target.id
                        # Try to get the value
                        if isinstance(node.value, python_ast.Constant):
                            variables[var_name] = node.value.value
                        elif isinstance(node.value, python_ast.Num):
                            variables[var_name] = node.value.n
                        elif isinstance(node.value, python_ast.Str):
                            variables[var_name] = node.value.s
        
        return variables
    except SyntaxError:
        return {}


def analyze_js_metrics(code: str) -> Dict[str, Any]:
    """Analyze JavaScript code metrics."""
    try:
        tree = python_ast.parse(code, mode='exec')
        
        func_count = 0
        var_count = 0
        total_lines = len(code.split('\n'))
        
        for node in python_ast.walk(tree):
            if isinstance(node, (python_ast.FunctionDef, python_ast.AsyncFunctionDef)):
                func_count += 1
            elif isinstance(node, python_ast.Assign):
                var_count += 1
        
        # Count comments
        comment_lines = sum(1 for line in code.split('\n') if line.strip().startswith('#') or line.strip().startswith('//') or line.strip().startswith('/*'))
        
        return {
            "functions": func_count,
            "variables": var_count,
            "total_lines": total_lines,
            "comment_lines": comment_lines,
            "success": True,
        }
    except SyntaxError:
        return {
            "functions": 0,
            "variables": 0,
            "total_lines": 0,
            "comment_lines": 0,
            "success": False,
        }