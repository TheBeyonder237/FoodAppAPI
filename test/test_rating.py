from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)


def test_add_rating_data():
    payload = {"rating": 5, "comment": "Great work!"}
    response = client.post("/ratings/", json=payload)
    assert response.status_code == 200
    assert response.json()["detail"] == "Rating added successfully."


def test_get_ratings():
    response = client.get("/ratings/")
    assert response.status_code == 200
    assert response.json()["detail"] == "Ratings data retrieved successfully"


def test_get_rating_data():
    response = client.get("/ratings/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Rating doesn't exist."


def test_update_rating_data():
    payload = {"comment": "Updated comment"}
    response = client.put("/ratings/1", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "There was an error updating the rating data."


def test_delete_rating_data():
    response = client.delete("/ratings/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Rating with id 1 doesn't exist"
