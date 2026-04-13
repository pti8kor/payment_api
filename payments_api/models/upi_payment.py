from dataclasses import dataclass

from payments_api.models.payment import Payment


@dataclass
class UPIPayment(Payment):
    upi_id: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if not self.upi_id.strip() or "@" not in self.upi_id:
            raise ValueError("A valid UPI ID is required")

    def process_payment(self) -> str:
        return f"Processed UPI payment of {self.amount} {self.currency} for {self.upi_id}"
