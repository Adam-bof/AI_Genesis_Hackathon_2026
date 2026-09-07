"""
API routes for Code Quality Agent
"""

from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..tools import code_analyzer_tool, performance_profiler_tool, security_scanner_tool, fix_suggester_tool

router = APIRouter(prefix="/api/v1", tags=["code-quality"])


@router.post("/analyze")
async def analyze_code(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Analyze uploaded code file."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    
    code = content.decode("utf-8", errors="replace")
    
    # Use language from filename or default to python
    language = "python"  # TODO: detect from file extension
    
    # Run code analyzer
    analysis = code_analyzer_tool.analyze(code, language)
    
    # Run performance profiler
    performance = performance_profiler_tool.profile(code, language)
    
    # Run security scanner
    security = security_scanner_tool.scan(code, language)
    
    return {
        "language": language,
        "analysis": analysis,
        "performance": performance,
        "security": security,
        "file_size": len(content),
    }


@router.post("/security-scan")
async def security_scan(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Security-specific scan of code file."""
    content = await file.read()
    code = content.decode("utf-8", errors="replace")
    language = "python"
    
    result = security_scanner_tool.scan(code, language)
    return result


@router.post("/fix-suggestions")
async def fix_suggestions(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Get fix suggestions for code issues."""
    content = await file.read()
    code = content.decode("utf-8", errors="replace")
    language = "python"
    
    # First analyze to get metrics
    analysis = code_analyzer_tool.analyze(code, language)
    
    # Get fix suggestions
    result = fix_suggester_tool.suggest_fixes(code, analysis.get("quality_issues", []), language)
    
    return result


@router.get("/health")
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "code-quality-agent"}