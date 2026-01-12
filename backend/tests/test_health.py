# backend/tests/test_health.py
"""
Health check test for the Financial QA FastAPI app.

Purpose:
- Verifies that the FastAPI app is running.
- Confirms the root endpoint ("/") or "/health" returns a 200 OK response.
- Serves as a basic smoke test for CI/CD pipelines.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app

# Create a TestClient instance to simulate HTTP requests
client = TestClient(app)


def test_health_endpoint():
    """
    Sends a GET request to the root ("/") endpoint.
    Expects a 200 OK response with a JSON body indicating status.
    """
    response = client.get("/")  # or "/health" if you prefer
    assert response.status_code == 200, "Root endpoint should return HTTP 200"

    data = response.json()
    assert "status" in data, "Response JSON must contain 'status'"
    assert data["status"] == "ok", "Health check status should be 'ok'"
