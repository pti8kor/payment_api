from payments_api.models.credit_card_payment import CreditCardPayment
from payments_api.models.payment import Payment
from payments_api.models.paypal_payment import PayPalPayment
from payments_api.models.upi_payment import UPIPayment


def create_credit_card_payment(
    amount: float,
    currency: str,
    *,
    card_number: str,
    cardholder_name: str,
    expiry_date: str,
) -> Payment:
    return CreditCardPayment(amount, currency, card_number, cardholder_name, expiry_date)


def create_paypal_payment(amount: float, currency: str, *, email: str) -> Payment:
    return PayPalPayment(amount, currency, email)


def create_upi_payment(amount: float, currency: str, *, upi_id: str) -> Payment:
    return UPIPayment(amount, currency, upi_id)
