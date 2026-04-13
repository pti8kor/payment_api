from dataclasses import dataclass

from payments_api.models.payment import Payment


@dataclass
class CreditCardPayment(Payment):
    card_number: str
    cardholder_name: str
    expiry_date: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.card_number.strip():
            raise ValueError("Card number is required")
        if not self.cardholder_name.strip():
            raise ValueError("Cardholder name is required")
        if not self.expiry_date.strip():
            raise ValueError("Expiry date is required")

    def process_payment(self) -> str:
        return (
            f"Processed credit card payment of {self.amount} "
            f"{self.currency} for {self.cardholder_name}"
        )
