import pytest

@pytest.fixture
def auth_headers(client):
    # Register a standard user
    client.post(
        "/api/auth/register",
        json={"username": "normaluser", "email": "normal@test.com", "password": "password123"}
    )
    # Login to get token
    response = client.post(
        "/api/auth/login",
        data={"username": "normaluser", "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_problem_unauthorized(client, auth_headers):
    # A normal Contestant should get 403 Forbidden
    problem_data = {
        "title": "Test Problem",
        "description": "Desc",
        "input_spec": "In",
        "output_spec": "Out",
        "difficulty": "Easy",
        "category": "Arrays",
        "is_published": True
    }
    response = client.post("/api/problems/", json=problem_data, headers=auth_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"
