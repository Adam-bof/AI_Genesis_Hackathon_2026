"""
Core analyzer - combines parsing, metrics, and AI analysis.

Supports Python, C, and JavaScript as defined in the hackathon plan.
"""

from fastapi import HTTPException, UploadFile
import tempfile
import os
from typing import Dict, List, Any

# Import parsers directly from their modules
from app.parsers.python_parser import parse_python, extract_functions as py_extract_functions, extract_classes as py_extract_classes
from app.parsers.c_parser import parse_c, extract_functions as c_extract_functions, extract_types, analyze_c_metrics
from app.parsers.js_parser import parse_javascript, extract_functions as js_extract_functions, extract_variables, analyze_js_metrics
from app.metrics.metrics import analyze_code_metrics as base_metrics
from app.tools import code_analyzer_tool, performance_profiler_tool, security_scanner_tool, fix_suggester_tool


class CodeAnalyzer:
    """Main analyzer that orchestrates code analysis pipeline for multiple languages."""
    
    def __init__(self):
        self.parsers = {}
        self.metrics_calculators = {}
        self.ai_client = None
        self.tools = {}
    
    async def analyze(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Run full analysis on code."""
        results = {
            "language": language,
            "quality_issues": [],
            "performance_issues": [],
            "security_issues": [],
            "fix_suggestions": [],
            "metrics": {}
        }
        
        # Parse code based on language
        if language == "python":
            ast = parse_python(code)
            results["functions"] = py_extract_functions(ast)
            results["classes"] = py_extract_classes(ast)
            
        elif language == "c":
            results["asts_c"] = parse_c(code)
            metrics = analyze_c_metrics(code)
            results["functions"] = c_extract_functions(results["asts_c"]) if results["asts_c"] else []
            results["types"] = extract_types(code) if results["asts_c"] else {}
            
        elif language == "javascript":
            ast = parse_javascript(code)
            if ast:
                results["functions"] = js_extract_functions(ast)
                results["variables"] = extract_variables(code)
            else:
                results["functions"] = []
                results["variables"] = {}
        
        # Calculate metrics
        results["metrics"] = base_metrics(code)
        
        # Detect quality issues
        analysis = code_analyzer_tool.analyze(code, language)
        results["quality_issues"] = analysis.get("quality_issues", [])
        results["performance_issues"] = analysis.get("performance_issues", [])
        results["security_issues"] = analysis.get("security_issues", [])
        
        # Get fix suggestions
        results["fix_suggestions"] = fix_suggester_tool.suggest_fixes(
            code, results["quality_issues"], language
        )
        
        return results
    
    def register_tool(self, name: str, tool_func):
        """Register an analysis tool."""
        self.tools[name] = tool_func