from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)


def test_add_new_user_data():
    payload = {
                "username": "david",
                "email": "user@email.com",
                "password": "string",
                "fullname": "string",
                "bio": "string",
                "profile_image": "string"}
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    assert response.json() == "user added successfully."


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["detail"] == "Users data retrieved successfully"

