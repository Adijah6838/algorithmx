def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_user(client):
    # Register first time
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    # Try to register again
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user(client):
    # Register
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client):
    client.post(
        "/api/auth/register",
        json={"username": "testuser", "email": "test@test.com", "password": "password123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
