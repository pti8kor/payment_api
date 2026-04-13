import pytest

from payments_api.models.credit_card_payment import CreditCardPayment
from payments_api.models.paypal_payment import PayPalPayment
from payments_api.models.upi_payment import UPIPayment


# ---------------------------------------------------------------------------
# Base Payment validation (tested through a concrete subclass)
# ---------------------------------------------------------------------------


def test_payment_rejects_zero_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be greater than 0"):
        CreditCardPayment(0, "USD", "4111111111111111", "Test User", "12/29")


def test_payment_rejects_negative_amount() -> None:
    with pytest.raises(ValueError, match="Amount must be greater than 0"):
        CreditCardPayment(-5.0, "USD", "4111111111111111", "Test User", "12/29")


def test_payment_rejects_empty_currency() -> None:
    with pytest.raises(ValueError, match="Currency must be a non-empty string"):
        CreditCardPayment(100, "", "4111111111111111", "Test User", "12/29")


def test_payment_rejects_blank_currency() -> None:
    with pytest.raises(ValueError, match="Currency must be a non-empty string"):
        CreditCardPayment(100, "   ", "4111111111111111", "Test User", "12/29")


# ---------------------------------------------------------------------------
# CreditCardPayment
# ---------------------------------------------------------------------------


def test_credit_card_payment_success() -> None:
    payment = CreditCardPayment(150.0, "USD", "4111111111111111", "Alice Smith", "12/29")

    result = payment.process_payment()

    assert "150.0" in result
    assert "USD" in result
    assert "Alice Smith" in result


def test_credit_card_rejects_blank_card_number() -> None:
    with pytest.raises(ValueError, match="Card number is required"):
        CreditCardPayment(100, "USD", "   ", "Test User", "12/29")


def test_credit_card_rejects_blank_cardholder_name() -> None:
    with pytest.raises(ValueError, match="Cardholder name is required"):
        CreditCardPayment(100, "USD", "4111111111111111", "   ", "12/29")


def test_credit_card_rejects_blank_expiry_date() -> None:
    with pytest.raises(ValueError, match="Expiry date is required"):
        CreditCardPayment(100, "USD", "4111111111111111", "Test User", "   ")


# ---------------------------------------------------------------------------
# PayPalPayment
# ---------------------------------------------------------------------------


def test_paypal_payment_success() -> None:
    payment = PayPalPayment(75.0, "EUR", "user@example.com")

    result = payment.process_payment()

    assert "75.0" in result
    assert "EUR" in result
    assert "user@example.com" in result


def test_paypal_rejects_email_without_at_sign() -> None:
    with pytest.raises(ValueError, match="valid PayPal email"):
        PayPalPayment(100, "USD", "not-an-email")


def test_paypal_rejects_blank_email() -> None:
    with pytest.raises(ValueError, match="valid PayPal email"):
        PayPalPayment(100, "USD", "   ")


# ---------------------------------------------------------------------------
# UPIPayment
# ---------------------------------------------------------------------------


def test_upi_payment_success() -> None:
    payment = UPIPayment(500.0, "INR", "user@upi")

    result = payment.process_payment()

    assert "500.0" in result
    assert "INR" in result
    assert "user@upi" in result


def test_upi_rejects_id_without_at_sign() -> None:
    with pytest.raises(ValueError, match="valid UPI ID"):
        UPIPayment(100, "INR", "invalitupiid")


def test_upi_rejects_blank_upi_id() -> None:
    with pytest.raises(ValueError, match="valid UPI ID"):
        UPIPayment(100, "INR", "   ")
