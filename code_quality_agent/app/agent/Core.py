"""
AI Agent Core - Claude/GPT-4 integration for code analysis and fix suggestions.

As defined in the hackathon plan (Phase 3: Initial Build and Phase 4: Tool Development):
- Basic Agent: Claude integration without tools (Phase 3)
- Agentic Tools development (Phase 4)
- AI Agent Core with decision making (Phase 4+)
"""

import json
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime


class AgentCore:
    """Core AI reasoning engine for the Code Quality Agent."""
    
    def __init__(self, 
                 claude_api_key: Optional[str] = None,
                 openai_api_key: Optional[str] = None):
        self.claude_api_key = claude_api_key
        self.openai_api_key = openai_api_key
        self.initialized = False
        
        # Agent configuration as per plan
        self.max_iterations = 10
        self.context_window = 100000  # tokens
        self.tools_registered = {}
    
    async def initialize(self):
        """Initialize the AI agent core."""
        self.initialized = True
        # TODO: Actually initialize Claude/GPT-4 clients
        # from anthropic import Anthropic
        # self.anthropic = Anthropic(api_key=self.claude_api_key)
        # from openai import OpenAI
        # self.openai = OpenAI(api_key=self.openai_api_key)
    
    async def analyze_code_with_ai(self, 
                                   code: str, 
                                   metrics: Dict[str, Any], 
                                   performance_issues: List[Dict],
                                   security_issues: List[Dict]) -> Dict[str, Any]:
        """Use Claude/GPT-4 to analyze code and generate fix suggestions."""
        
        if not self.initialized:
            await self.initialize()
        
        # Build the prompt for the AI
        prompt = self._build_analysis_prompt(
            code, metrics, performance_issues, security_issues
        )
        
        # TODO: Call Claude or OpenAI API
        # For now, return structured analysis
        return self._fallback_analysis(code, metrics, performance_issues, security_issues)
    
    def _build_analysis_prompt(self, code, metrics, performance_issues, security_issues):
        """Build the prompt for AI analysis."""
        return f"""
        You are an expert code reviewer. Analyze the following code and provide detailed feedback.

        CODE:
        ```python
        {code}
        ```

        METRICS:
        - Cyclomatic complexity: {metrics.get('complexity', [])}
        - Maintainability index: {metrics.get('maintainability', {}).get('mi', 'N/A')}
        - Lines of code: {metrics.get('loc', {}).get('total_lines', 'N/A')}

        PERFORMANCE ISSUES:
        {performance_issues}

        SECURITY ISSUES:
        {security_issues}

        Please provide:
        1. Priority-ordered list of issues (critical → low)
        2. Technical explanation for each issue
        3. Code examples with fixes
        4. Performance impact estimation (if applicable)
        5. Maintainability impact
        """

    def _fallback_analysis(self, code, metrics, performance_issues, security_issues):
        """Fallback analysis when AI is not available."""
        return {
            "ai_reasoning_available": False,
            "analysis": self._generate_basic_analysis(code, metrics, performance_issues, security_issues),
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def _generate_basic_analysis(self, code, metrics, performance_issues, security_issues):
        """Generate basic analysis without AI."""
        issues = []
        
        # Add security issues
        for sec in security_issues:
            issues.append({
                "priority": "critical" if sec.get("severity") == "critical" else "high",
                "type": sec.get("type", "unknown"),
                "description": sec.get("description", "Security issue detected"),
                "severity": sec.get("severity", "medium"),
            })
        
        # Add performance issues
        for perf in performance_issues:
            issues.append({
                "priority": "medium",
                "type": perf.get("type", "performance"),
                "description": perf.get("description", "Performance issue"),
                "severity": "medium",
            })
        
        # Add metrics-based issues
        complexity = metrics.get("complexity", [])
        if complexity:
            avg_complexity = sum(c.get("complexity", 0) for c in complexity) / len(complexity)
            if avg_complexity > 10:
                issues.append({
                    "priority": "high",
                    "type": "high_complexity",
                    "description": f"Average cyclomatic complexity is {avg_complexity:.1f} (above 10)",
                    "severity": "high",
                })
        
        return {
            "issues": sorted(issues, key=lambda x: x["priority"]),
            "summary": {
                "total_issues": len(issues),
                "critical": sum(1 for i in issues if i["priority"] == "critical"),
                "high": sum(1 for i in issues if i["priority"] == "high"),
                "medium": sum(1 for i in issues if i["priority"] == "medium"),
            }
        }
    
    async def suggest_fixes_with_ai(self, 
                                    code: str, 
                                    issues: List[Dict]) -> Dict[str, Any]:
        """Use AI to suggest fixes for identified issues."""
        
        if not self.initialized:
            await self.initialize()
        
        prompt = self._build_fix_prompt(code, issues)
        
        # TODO: Call Claude/GPT-4 API
        return self._fallback_fix_suggestions(code, issues)
    
    def _build_fix_prompt(self, code, issues):
        """Build the fix suggestion prompt."""
        issues_summary = "\n".join([
            f"- {i.get('type')}: {i.get('description')}" 
            for i in issues[:10]  # Limit to top 10 issues
        ])
        
        return f"""
        You are a senior software engineer. Provide fixes for the following code issues.

        CODE:
        ```python
        {code}
        ```

        ISSUES TO FIX:
        {issues_summary}

        For each issue, provide:
        1. A clear explanation of the problem
        2. Python code example showing the fix
        3. The performance/maintainability benefit of the fix
        4. Why this fix works

        Format as JSON with structure:
        {{
          "fixes": [
            {{
              "issue_type": "string",
              "explanation": "string",
              "fixed_code": "string",
              "benefit": "string"
            }}
          ]
        }}
        """
    
    def _fallback_fix_suggestions(self, code, issues):
        """Fallback fix suggestions without AI."""
        fixes = []
        
        for issue in issues[:5]:  # Limit to top 5
            issue_type = issue.get("type", "unknown")
            
            if issue_type == "high_complexity":
                fixes.append({
                    "issue_type": "high_complexity",
                    "explanation": "Function has high cyclomatic complexity, making it hard to understand and maintain",
                    "fixed_code": "// Consider extracting sub-functions or using strategy pattern\n// Original: complex function\n// Fixed: broken into smaller, single-responsibility functions",
                    "benefit": "Improved readability, easier testing, better maintainability"
                })
            elif issue_type == "hardcoded_credential":
                fixes.append({
                    "issue_type": "hardcoded_credential",
                    "explanation": "Credentials hardcoded in source code pose security risk",
                    "fixed_code": "import os\nAPI_KEY = os.getenv('API_KEY')\n# Use: API_KEY instead of hardcoded value",
                    "benefit": "Credentials no longer in source code; can be rotated without code changes"
                })
            elif issue_type == "potential_o_n2_loop":
                fixes.append({
                    "issue_type": "potential_o_n2_loop",
                    "explanation": "Nested loops may result in O(n²) performance",
                    "fixed_code": "// Use set/dict lookup for O(1) membership testing\n# Original: nested loop\n# Fixed: use set for O(n) overall",
                    "benefit": "Performance improved from O(n²) to O(n)"
                })
            else:
                fixes.append({
                    "issue_type": issue_type,
                    "explanation": f"Issue: {issue.get('description', 'Unknown issue')}",
                    "fixed_code": "// Fix to be determined",
                    "benefit": "Issue resolved"
                })
        
        return {
            "fixes": fixes,
            "total_fixes": len(fixes),
            "ai_reasoning_available": False
        }