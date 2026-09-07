"""
Core analyzer - combines parsing, metrics, and AI analysis.

Supports Python, C, and JavaScript as defined in the hackathon plan.
Phase 4: Tool development with multi-language support.
"""

import asyncio
from typing import Dict, List, Any, Optional

# Use absolute imports since this can be imported directly or as part of app.core package
from app.parsers.python_parser import parse_python, extract_functions as py_extract_functions, extract_classes as py_extract_classes
from app.parsers.c_parser import parse_c, extract_functions as c_extract_functions, extract_types, analyze_c_metrics
from app.parsers.js_parser import parse_javascript, extract_functions as js_extract_functions, extract_variables, analyze_js_metrics
from app.metrics.metrics import analyze_code_metrics as base_metrics
from app.tools import code_analyzer_tool, performance_profiler_tool, security_scanner_tool, fix_suggester_tool
from app.agent.Core import AgentCore


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
            c_ast = parse_c(code)
            results["functions"] = c_extract_functions(c_ast) if c_ast else []
            results["types"] = extract_types(code) if c_ast else {}
            
        elif language == "javascript":
            js_ast = parse_javascript(code)
            if js_ast:
                results["functions"] = js_extract_functions(js_ast)
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