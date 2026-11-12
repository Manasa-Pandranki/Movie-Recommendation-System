from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_create_movie():
    response = client.post(
        "/movies",
        json={
            "title": "Pytest Demo Movie",
            "genre": "Action"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Pytest Demo Movie"
def test_user_registration():
    response = client.post(
        "/auth/register",
        json={
            "username": "pytest_user",
            "email": "pytest_user_2026@example.com",
            "password": "TestPass123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"