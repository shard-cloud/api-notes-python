"""
Notes API tests
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def auth_headers(client):
    """Get authentication headers"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = client.post("/auth/token", json=login_data)
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


def test_create_note(client, auth_headers):
    """Test creating a note"""
    note_data = {
        "title": "Test Note",
        "content": "This is a test note"
    }
    
    response = client.post("/notes/", json=note_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note"
    assert "id" in data
    assert "created_at" in data


def test_get_notes(client, auth_headers):
    """Test getting notes list"""
    response = client.get("/notes/", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert isinstance(data["items"], list)


def test_get_note_by_id(client, auth_headers):
    """Test getting a specific note"""
    # First create a note
    note_data = {
        "title": "Test Note for Get",
        "content": "Content for get test"
    }
    
    create_response = client.post("/notes/", json=note_data, headers=auth_headers)
    note_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == note_id
    assert data["title"] == "Test Note for Get"


def test_update_note(client, auth_headers):
    """Test updating a note"""
    # First create a note
    note_data = {
        "title": "Original Title",
        "content": "Original content"
    }
    
    create_response = client.post("/notes/", json=note_data, headers=auth_headers)
    note_id = create_response.json()["id"]
    
    # Then update it
    update_data = {
        "title": "Updated Title",
        "content": "Updated content"
    }
    
    response = client.put(f"/notes/{note_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_delete_note(client, auth_headers):
    """Test deleting a note"""
    # First create a note
    note_data = {
        "title": "Note to Delete",
        "content": "This note will be deleted"
    }
    
    create_response = client.post("/notes/", json=note_data, headers=auth_headers)
    note_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/notes/{note_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/notes/{note_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_get_nonexistent_note(client, auth_headers):
    """Test getting a note that doesn't exist"""
    response = client.get("/notes/99999", headers=auth_headers)
    assert response.status_code == 404


def test_search_notes(client, auth_headers):
    """Test searching notes"""
    # Create a note with specific content
    note_data = {
        "title": "Search Test Note",
        "content": "This note contains searchable content"
    }
    
    client.post("/notes/", json=note_data, headers=auth_headers)
    
    # Search for it
    response = client.get("/notes/?search=searchable", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["items"]) >= 1
    assert any("searchable" in note["content"] for note in data["items"])


def test_pagination(client, auth_headers):
    """Test pagination"""
    response = client.get("/notes/?page=1&limit=5", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 5
    assert len(data["items"]) <= 5
