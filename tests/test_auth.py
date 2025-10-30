"""
Authentication tests
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_username(client):
    """Test registration with duplicate username"""
    user_data = {
        "username": "admin",
        "email": "admin2@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]


def test_login_success(client):
    """Test successful login"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = client.post("/auth/token", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    login_data = {
        "username": "admin",
        "password": "wrongpassword"
    }
    
    response = client.post("/auth/token", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/notes/")
    assert response.status_code == 401


def test_protected_endpoint_with_token(client):
    """Test accessing protected endpoint with valid token"""
    # First login to get token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    login_response = client.post("/auth/token", json=login_data)
    token = login_response.json()["access_token"]
    
    # Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
