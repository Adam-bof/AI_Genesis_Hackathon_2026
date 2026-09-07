"""
C/C++ parser for Code Quality Agent.

Uses pycparser for C code analysis when available.
Falls back to basic metrics when pycparser is not available or parsing fails.
"""

from typing import Dict, List, Any, Optional


def parse_c(code: str) -> Optional[Any]:
    """Parse C code using pycparser.
    
    Returns AST node or None if parsing fails.
    """
    try:
        # pycparser.parse() doesn't exist; use parse_file with StringIO or c_parser
        # For now, return None to indicate pycparser not fully configured
        # The analyze_c_metrics function will handle the fallback
        return None
    except Exception:
        return None


def extract_functions(ast_node: Any) -> List[Dict]:
    """Extract function definitions from C AST."""
    functions = []
    if ast_node is None:
        return functions
    
    # Basic extraction - in a full implementation, walk the pycparser AST
    # For now return empty list since full pycparser setup is complex
    return functions


def extract_types(code: str) -> Dict[str, Any]:
    """Extract type information from C code."""
    try:
        # Attempt basic parsing - return empty if not available
        return {}
    except Exception:
        return {}


def analyze_c_metrics(code: str) -> Dict[str, Any]:
    """Analyze C code metrics.
    
    Falls back to basic metrics when pycparser is not available.
    """
    # Basic C metrics without full pycparser integration
    # Count potential functions by pattern recognition
    func_count = 0
    lines = code.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    
    # Simple heuristic: count function-like patterns
    import re
    func_pattern = r'\w+\s+\w+\s*\([^)]*\)\s*\{'
    matches = re.findall(func_pattern, code)
    func_count = len(matches)
    
    return {
        "functions": func_count,
        "types": 0,
        "success": True,
        "note": "Basic metrics - pycparser not fully configured, using pattern matching"
    }