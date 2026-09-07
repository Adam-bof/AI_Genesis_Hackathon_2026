"""
API Specification for Code Quality Agent
OpenAPI/Swagger specification as defined in Phase 2: Technical Design
"""

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

app = FastAPI(
    title="Autonomous Code Quality & Performance Agent API",
    description="API for analyzing code quality, performance, and security issues",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Endpoints defined in Phase 3: Initial Build
"""
Endpoint: GET /
Description: Root endpoint - returns service status
Responses:
  200: {"message": "Code Quality Agent API is running"}

Endpoint: GET /health
Description: Health check endpoint
Responses:
  200: {"status": "healthy", "service": "code-quality-agent"}

Endpoint: POST /api/v1/analyze
Description: Analyze uploaded code file
Parameters:
  - file: UploadFile - the code file to analyze
Responses:
  200: {
    "language": "python",
    "analysis": {"metrics": ..., "complexity_score": float, "maintainability_index": float, "loc": int},
    "performance": {"performance_issues": [...], "bottlenecks_detected": int},
    "security": {"vulnerabilities": [...], "security_issues_found": int},
    "file_size": int
  }

Endpoint: POST /api/v1/security-scan
Description: Security-specific scan of code file
Parameters:
  - file: UploadFile - the code file to scan
Responses:
  200: {"vulnerabilities": [...], "security_issues_found": int}

Endpoint: POST /api/v1/fix-suggestions
Description: Get fix suggestions for code issues
Parameters:
  - file: UploadFile - the code file to get fixes for
Responses:
  200: {"suggestions": [...], "total_fixes": int}
"""