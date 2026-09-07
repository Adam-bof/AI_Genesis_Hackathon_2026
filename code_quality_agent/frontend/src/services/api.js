/**
 * API service for communicating with the Code Quality Agent backend.
 * All endpoints use the FastAPI backend running on port 8000.
 */

const API_BASE = "http://localhost:8000/api";

export const analyzeCode = async (code, language) => {
  const formData = new FormData();
  formData.append("file", new Blob([code], { type: "text/plain" }), "code." + language);

  const response = await fetch(`${API_BASE}/v1/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Analysis failed");
  }

  return response.json();
};

export const securityScan = async (code, language) => {
  const formData = new FormData();
  formData.append("file", new Blob([code], { type: "text/plain" }), "code." + language);

  const response = await fetch(`${API_BASE}/v1/security-scan`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Security scan failed");
  }

  return response.json();
};

export const getFixSuggestions = async (code, language, issues) => {
  const formData = new FormData();
  formData.append("file", new Blob([code], { type: "text/plain" }), "code." + language);

  const response = await fetch(`${API_BASE}/v1/fix-suggestions`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Fix suggestions failed");
  }

  return response.json();
};