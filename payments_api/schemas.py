from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, field_validator


class BasePaymentRequest(BaseModel):
    payment_type: str
    amount: float
    currency: str

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Currency must be a non-empty string")
        return value.strip().upper()


class CreditCardPaymentRequest(BasePaymentRequest):
    payment_type: Literal["credit_card"]
    card_number: str
    cardholder_name: str
    expiry_date: str


class PayPalPaymentRequest(BasePaymentRequest):
    payment_type: Literal["paypal"]
    email: str


class UPIPaymentRequest(BasePaymentRequest):
    payment_type: Literal["upi"]
    upi_id: str


PaymentRequest = Annotated[
    Union[CreditCardPaymentRequest, PayPalPaymentRequest, UPIPaymentRequest],
    Field(discriminator="payment_type"),
]
