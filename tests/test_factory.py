import pytest

from payments_api.factory import PaymentFactory
from payments_api.models.payment import Payment


class DummyPayment(Payment):
    def process_payment(self) -> str:
        return "dummy"


@pytest.fixture(autouse=True)
def reset_factory_registry():
    original = PaymentFactory._creators.copy()
    yield
    PaymentFactory._creators = original


def test_register_payment_normalizes_type() -> None:
    PaymentFactory.register_payment("  custom_type  ", lambda amount, currency: DummyPayment(amount, currency))

    assert "custom_type" in PaymentFactory._creators


def test_register_payment_rejects_empty_type() -> None:
    with pytest.raises(ValueError, match="Payment type cannot be empty"):
        PaymentFactory.register_payment("   ", lambda amount, currency: DummyPayment(amount, currency))


def test_create_payment_returns_payment_instance() -> None:
    PaymentFactory.register_payment("custom", lambda amount, currency: DummyPayment(amount, currency))

    payment = PaymentFactory.create_payment("custom", 10.0, "USD")

    assert isinstance(payment, DummyPayment)


def test_create_payment_unknown_type_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Invalid payment type"):
        PaymentFactory.create_payment("unknown", 10.0, "USD")


def test_create_payment_invalid_creator_args_raises_value_error() -> None:
    def creator(amount: float, currency: str, *, required_flag: str) -> DummyPayment:
        return DummyPayment(amount, currency)

    PaymentFactory.register_payment("custom", creator)

    with pytest.raises(ValueError, match="Invalid arguments"):
        PaymentFactory.create_payment("custom", 10.0, "USD")
