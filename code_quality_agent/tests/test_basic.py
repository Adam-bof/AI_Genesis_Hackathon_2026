"""
Test the Code Quality Agent backend
"""

import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "code-quality-agent"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Code Quality Agent API is running"


def test_analyze_endpoint():
    """Test code analysis endpoint."""
    code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    result = 0
    for i in range(2, n + 1):
        result += calculate_fibonacci(i - 1) + calculate_fibonacci(i - 2)
    return result
"""
    
    response = client.post(
        "/api/v1/analyze",
        files={"file.py": code.encode("utf-8")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "language" in data
    assert "analysis" in data
    assert "performance" in data
    assert "security" in data


def test_security_scan():
    """Test security scan endpoint."""
    code = "API_KEY = 'sk-abc123xyz'"
    
    response = client.post(
        "/api/v1/security-scan",
        files={"file.py": code.encode("utf-8")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "vulnerabilities" in data


def test_fix_suggestions():
    """Test fix suggestions endpoint."""
    code = "result = eval(user_input)"
    
    response = client.post(
        "/api/v1/fix-suggestions",
        files={"file.py": code.encode("utf-8")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data