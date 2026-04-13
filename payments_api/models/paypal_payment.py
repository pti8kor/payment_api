from dataclasses import dataclass

from payments_api.models.payment import Payment


@dataclass
class PayPalPayment(Payment):
    email: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.email.strip() or "@" not in self.email:
            raise ValueError("A valid PayPal email is required")

    def process_payment(self) -> str:
        return f"Processed PayPal payment of {self.amount} {self.currency} for {self.email}"
