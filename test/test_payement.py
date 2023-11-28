import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from server.app import app


@pytest.fixture
def client():
    return TestClient(app)


@patch("app.httpx.AsyncClient")
def test_initialize_payment(mock_async_client, client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"transaction": {"reference": "abc123"}}
    mock_async_client.return_value.post.return_value = mock_response

    payload = {
        "user_id": "123",
        "userEmail": "user@example.com",
        "paymentAmount": 50.0,
    }

    response = client.post("/initialize_payment/", json=payload)

    mock_async_client.return_value.post.assert_called_once()
    assert response.status_code == 200
    assert "payment_link" in response.json()


@patch("app.verify_payment_status")
@patch("app.update_payment")
@patch("app.add_subscription_after_payment")
async def test_callback_handler(mock_add_subscription, mock_update_payment, mock_verify_payment, client):
    transaction_id = "123"
    callback_url = f"/payment_callback/?tid={transaction_id}"
    signature = "valid_signature"

    mock_request = MagicMock()
    mock_request.body = b"request_body"
    mock_request.headers.get.return_value = signature

    mock_verify_payment.return_value = {"status": True, "transaction": {"transaction": {"status": "successful"}}}

    response = await client.get(callback_url, headers={"x-notch-signature": signature}, request=mock_request)

    mock_verify_payment.assert_called_once_with("abc123")
    mock_update_payment.assert_called_once()
    mock_add_subscription.assert_called_once()

    assert response.status_code == 200
    assert "Webhook processed successfully" in response.json()["message"]


@patch("app.verify_payment_status")
async def test_callback_handler_invalid_signature(mock_verify_payment, client):
    transaction_id = "123"
    callback_url = f"/payment_callback/?tid={transaction_id}"
    invalid_signature = "invalid_signature"

    mock_request = MagicMock()
    mock_request.headers.get.return_value = invalid_signature

    mock_verify_payment.return_value = {"status": True, "transaction": {"transaction": {"status": "successful"}}}

    response = await client.get(callback_url, headers={"x-notch-signature": invalid_signature}, request=mock_request)

    mock_verify_payment.assert_not_called()

    assert response.status_code == 403
    assert "Invalid signature" in response.json()["detail"]