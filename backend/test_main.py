from backend.recommendation import get_recommendations
from fastapi.testclient import TestClient
from backend.main import app
import uuid

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
    unique_id = uuid.uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"pytest_user_{unique_id}",
            "email": f"pytest_{unique_id}@example.com",
            "password": "TestPass123!"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"
def test_invalid_movie_id():
    response = client.get("/movies/999999")

    assert response.status_code == 404
def test_invalid_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "wrong_user@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401
def test_protected_endpoint_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401
def test_recommendations():
    response = client.get("/recommendations/1")

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "recommendations" in response.json()
    assert isinstance(response.json()["recommendations"], list)
def test_get_ratings():
    response = client.get("/ratings")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_new_user_popular_recommendations():
    recommendations = get_recommendations(999999, 5)

    assert isinstance(recommendations, list)
    assert len(recommendations) == 5
    assert all("title" in movie for movie in recommendations)
    assert all("movieId" in movie for movie in recommendations)