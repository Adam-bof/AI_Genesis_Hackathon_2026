"""
Metrics calculator with radon fallback.

Uses radon library for complexity calculation when available,
otherwise provides basic manual calculations.
"""

import ast
from typing import Dict, Any, List, Optional


def _calculate_complexity_manual(code: str) -> List[Dict]:
    """Manual cyclomatic complexity calculation when radon is not available."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    
    complexity_results = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Count decisions: if statements, for loops, while loops, try blocks
            # Base complexity is 1 for the function itself
            decisions = 1
            
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.If):
                    decisions += 1  # if adds 1 to complexity
                    # Check for elif/else in orelse
                    for orelse in child.orelse:
                        for nested in ast.walk(orelse):
                            if isinstance(nested, ast.If):
                                decisions += 1
                elif isinstance(child, ast.For):
                    decisions += 1
                elif isinstance(child, ast.While):
                    decisions += 1
                elif isinstance(child, ast.Try):
                    decisions += 1
                elif isinstance(child, ast.BoolOp):
                    # Each value in BooleanOp adds complexity
                    decisions += len(child.values) - 1
            
            complexity_results.append({
                "name": node.name,
                "lineno": node.lineno,
                "complexity": decisions,
            })
    
    return complexity_results


def _calculate_maintainability_manual(code: str) -> Dict[str, Any]:
    """Manual maintainability index when radon is not available."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"mi": 0, "grade": "F"}
    
    try:
        loc = len(code.split("\n"))
        complexity = 0
        
        # Count decision points
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                complexity += 1
            elif isinstance(node, ast.For):
                complexity += 1
            elif isinstance(node, ast.While):
                complexity += 1
            elif isinstance(node, ast.Try):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        # Simplified MI formula: MI = 171 - 5.2 * ln(halstead_volume) - 0.23 * halstead_difficulty
        # Simplified version using LOC and complexity
        if loc == 0:
            mi = 0
        else:
            # Simple approximation
            mi = max(0, 100 - (5 * complexity) - (0.25 * loc))
        
        mi = round(mi, 1)
        
        if mi >= 85:
            grade = "A"
        elif mi >= 65:
            grade = "B"
        elif mi >= 50:
            grade = "C"
        elif mi >= 35:
            grade = "D"
        else:
            grade = "F"
        
        return {"mi": mi, "grade": grade}
    except Exception:
        return {"mi": 0, "grade": "F"}


def calculate_cyclomatic_complexity(code: str) -> List[Dict]:
    """Calculate cyclomatic complexity, trying radon first, then manual fallback."""
    try:
        from radon.complexity import cc_analysis
        return cc_analysis(code)
    except ImportError:
        return _calculate_complexity_manual(code)


def calculate_maintainability_index(code: str) -> Dict[str, Any]:
    """Calculate maintainability index, trying radon first, then manual fallback."""
    try:
        from radon.metrics import mi_analysis
        return mi_analysis(code)
    except ImportError:
        return _calculate_maintainability_manual(code)


def count_lines_of_code(code: str) -> Dict[str, int]:
    """Count lines of code, blank lines, and comment lines."""
    lines = code.split("\n")
    blank_lines = sum(1 for line in lines if line.strip() == "")
    # Count both Python (#) and JavaScript (//, /* */) style comments
    comment_lines = sum(
        1 for line in lines 
        if line.strip().startswith('#') or 
           line.strip().startswith('//') or 
           line.strip().startswith('/*')
    )
    code_lines = len(lines) - blank_lines
    
    return {
        "total_lines": len(lines),
        "code_lines": code_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
    }


def analyze_code_metrics(code: str) -> Dict[str, Any]:
    """Run all metrics calculations on code."""
    return {
        "complexity": calculate_cyclomatic_complexity(code),
        "maintainability": calculate_maintainability_index(code),
        "loc": count_lines_of_code(code),
    }