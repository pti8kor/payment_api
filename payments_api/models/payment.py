from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Payment(ABC):
    amount: float
    currency: str

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self.currency or not self.currency.strip():
            raise ValueError("Currency must be a non-empty string")

    @abstractmethod
    def process_payment(self) -> str:
        """Process the payment and return a user-friendly message."""
