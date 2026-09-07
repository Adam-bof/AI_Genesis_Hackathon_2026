"""
Analysis tools for the Code Quality Agent.

Tools as defined in the hackathon plan:
- code_analyzer: analyzes code and extracts metrics
- performance_profiler: identifies bottlenecks
- security_scanner: detects vulnerabilities
- fix_suggester: suggests code examples with solutions
"""

from typing import Dict, Any, List
from .metrics.metrics import analyze_code_metrics


class CodeAnalyzerTool:
    """Code analyzer tool - extracts metrics and quality indicators."""
    
    def analyze(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze code and return metrics."""
        metrics = analyze_code_metrics(code)
        
        return {
            "metrics": metrics,
            "complexity_score": self._calculate_overall_complexity(metrics.get("complexity", [])),
            "maintainability_index": metrics.get("maintainability", {}).get("mi", 0),
            "loc": metrics.get("loc", {}).get("code_lines", 0),
        }
    
    def _calculate_overall_complexity(self, complexity_results: List[Dict]) -> float:
        """Calculate overall complexity score from radon results."""
        if not complexity_results:
            return 0.0
        total = sum(item["complexity"] for item in complexity_results)
        return round(total / len(complexity_results), 2)


class PerformanceProfilerTool:
    """Performance profiler - identifies bottlenecks and O(n²) patterns."""
    
    def profile(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Profile code for performance issues."""
        issues = []
        
        # Check for common Python performance anti-patterns
        if language == "python":
            # Look for O(n²) loops
            if "for" in code and "for" in code:
                # Simple heuristic: nested loops
                lines = code.split("\n")
                nested_loops = 0
                in_nested = False
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith("for "):
                        in_nested = True
                    elif in_nested and stripped.startswith(")"):
                        in_nested = False
                    elif in_nested and stripped.startswith("for "):
                        nested_loops += 1
                        in_nested = True
                
                if nested_loops > 0:
                    issues.append({
                        "type": "potential_o_n2_loop",
                        "description": f"Found {nested_loops} potential nested loop pattern",
                        "severity": "medium",
                    })
            
            # Look for unnecessary allocations
            if ".append(" in code or ".extend(" in code:
                issues.append({
                    "type": "unnecessary_allocation",
                    "description": "Consider list comprehension instead of append/extend loop",
                    "severity": "low",
                })
        
        return {
            "performance_issues": issues,
            "bottlenecks_detected": len(issues),
        }


class SecurityScannerTool:
    """Security scanner - detects common vulnerabilities."""
    
    def scan(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Scan code for security vulnerabilities."""
        vulnerabilities = []
        
        if language == "python":
            # Check for hardcoded credentials
            import re
            
            # Patterns that might indicate hardcoded secrets
            secret_patterns = [
                (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
                (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
                (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
                (r'token\s*=\s*["\'][^"\']+["\']', "Hardcoded token"),
            ]
            
            for pattern, description in secret_patterns:
                matches = re.findall(pattern, code, re.IGNORECASE)
                if matches:
                    vulnerabilities.append({
                        "type": "hardcoded_credential",
                        "description": f"{description} detected in code",
                        "severity": "critical",
                        "pattern_matches": len(matches),
                    })
            
            # Check for eval() usage
            if "eval(" in code:
                vulnerabilities.append({
                    "type": "eval_usage",
                    "description": "Use of eval() can lead to code injection",
                    "severity": "high",
                })
            
            # Check for exec() usage
            if "exec(" in code:
                vulnerabilities.append({
                    "type": "exec_usage",
                    "description": "Use of exec() can lead to code injection",
                    "severity": "high",
                })
        
        return {
            "vulnerabilities": vulnerabilities,
            "security_issues_found": len(vulnerabilities),
        }


class FixSuggesterTool:
    """Fix suggestor - provides code examples with solutions."""
    
    def suggest_fixes(self, code: str, issues: List[Dict], language: str = "python") -> Dict[str, Any]:
        """Suggest fixes for identified issues."""
        suggestions = []
        
        for issue in issues:
            issue_type = issue.get("type", "")
            
            if issue_type == "potential_o_n2_loop":
                suggestions.append({
                    "issue": issue,
                    "suggestion": "Replace nested loops with built-in functions or use set/dict lookups",
                    "example": {
                        "before": "```python\nfor i in range(len(arr)):\n    for j in range(i+1, len(arr)):\n        if arr[i] == arr[j]:\n            ...\n```",
                        "after": "```python\nseen = set()\nfor item in arr:\n    if item in seen:\n        ...\n    seen.add(item)\n```",
                    },
                    "performance_gain": "O(n) instead of O(n²)",
                })
            
            elif issue_type == "hardcoded_credential":
                suggestions.append({
                    "issue": issue,
                    "suggestion": "Move credentials to environment variables or secret manager",
                    "example": {
                        "before": "```python\nAPI_KEY = 'sk-abc123'\n```",
                        "after": "```python\nimport os\nAPI_KEY = os.getenv('API_KEY')\n```",
                    },
                    "security_gain": "Credentials no longer in source code",
                })
            
            elif issue_type == "eval_usage":
                suggestions.append({
                    "issue": issue,
                    "suggestion": "Replace eval() with ast.literal_eval() or explicit parsing",
                    "example": {
                        "before": "```python\nresult = eval(user_input)\n```",
                        "after": "```python\nimport ast\nresult = ast.literal_eval(user_input)\n```",
                    },
                    "security_gain": "Prevents code injection attacks",
                })
        
        return {
            "suggestions": suggestions,
            "total_fixes": len(suggestions),
        }


# Export all tools
code_analyzer_tool = CodeAnalyzerTool()
performance_profiler_tool = PerformanceProfilerTool()
security_scanner_tool = SecurityScannerTool()
fix_suggester_tool = FixSuggesterTool()