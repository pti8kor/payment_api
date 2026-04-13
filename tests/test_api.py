from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from payments_api.app import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_credit_card_payment_success() -> None:
    payload = {
        "payment_type": "credit_card",
        "amount": 100.5,
        "currency": "inr",
        "card_number": "4111111111111111",
        "cardholder_name": "Test User",
        "expiry_date": "12/29",
    }

    response = client.post("/payments/process", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["payment_type"] == "credit_card"
    assert data["amount"] == 100.5
    assert data["currency"] == "INR"
    assert "Processed credit card payment" in data["message"]


def test_process_payment_invalid_type_returns_422() -> None:
    payload = {
        "payment_type": "bank_transfer",
        "amount": 100,
        "currency": "USD",
    }

    response = client.post("/payments/process", json=payload)

    assert response.status_code == 422


def test_process_payment_negative_amount_returns_422() -> None:
    payload = {
        "payment_type": "paypal",
        "amount": -1,
        "currency": "USD",
        "email": "user@example.com",
    }

    response = client.post("/payments/process", json=payload)

    assert response.status_code == 422


def test_process_payment_missing_required_field_returns_422() -> None:
    payload = {
        "payment_type": "credit_card",
        "amount": 100,
        "currency": "USD",
        "card_number": "4111111111111111",
        "expiry_date": "12/29",
    }

    response = client.post("/payments/process", json=payload)

    assert response.status_code == 422


def test_process_paypal_invalid_email_returns_400() -> None:
    payload = {
        "payment_type": "paypal",
        "amount": 100,
        "currency": "USD",
        "email": "not-an-email",
    }

    response = client.post("/payments/process", json=payload)

    assert response.status_code == 400
    assert "PayPal email" in response.json()["detail"]


def test_process_payment_with_patched_factory() -> None:
    payload = {
        "payment_type": "paypal",
        "amount": 250.0,
        "currency": "usd",
        "email": "user@example.com",
    }

    mock_payment = Mock()
    mock_payment.process_payment.return_value = "mocked payment result"

    with patch("payments_api.app.PaymentFactory.create_payment", return_value=mock_payment) as mock_create:
        response = client.post("/payments/process", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "mocked payment result"
    mock_create.assert_called_once_with(
        "paypal",
        250.0,
        "USD",
        email="user@example.com",
    )
    mock_payment.process_payment.assert_called_once()


def test_process_payment_with_patched_factory_error_returns_400() -> None:
    payload = {
        "payment_type": "paypal",
        "amount": 250.0,
        "currency": "usd",
        "email": "user@example.com",
    }

    with patch.object(client, "post", wraps=client.post) as post_spy:
        with patch(
            "payments_api.app.PaymentFactory.create_payment",
            side_effect=ValueError("mocked factory failure"),
        ) as mock_create:
            response = client.post("/payments/process", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "mocked factory failure"
    post_spy.assert_called_once_with("/payments/process", json=payload)
    mock_create.assert_called_once_with(
        "paypal",
        250.0,
        "USD",
        email="user@example.com",
    )
