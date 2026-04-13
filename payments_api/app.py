from fastapi import FastAPI, HTTPException

from payments_api.creators import (
    create_credit_card_payment,
    create_paypal_payment,
    create_upi_payment,
)
from payments_api.factory import PaymentFactory
from payments_api.logging_config import get_logger, setup_logging
from payments_api.schemas import PaymentRequest


setup_logging()
logger = get_logger(__name__)

app = FastAPI(title="Payments API", version="1.0.0")


PaymentFactory.register_payment("credit_card", create_credit_card_payment)
PaymentFactory.register_payment("paypal", create_paypal_payment)
PaymentFactory.register_payment("upi", create_upi_payment)
logger.info("Payment types registered: credit_card, paypal, upi")


@app.post("/payments/process")
def process_payment(request: PaymentRequest) -> dict[str, str | float]:
    # BREAKPOINT 1: Step here to see the incoming request payload
    payload = request.model_dump()
    logger.info(
        "Received payment request | type=%s amount=%.2f currency=%s",
        request.payment_type,
        request.amount,
        request.currency,
    )
    kwargs = {
        key: value
        for key, value in payload.items()
        if key not in {"payment_type", "amount", "currency"}
    }

    try:
        # BREAKPOINT 2: Step here to trace factory.create_payment() call
        payment = PaymentFactory.create_payment(
            request.payment_type,
            request.amount,
            request.currency,
            **kwargs,
        )
        # BREAKPOINT 3: After factory returns, inspect the payment object type
        result = payment.process_payment()
        logger.info(
            "Payment processed successfully | type=%s message=%s",
            request.payment_type,
            result,
        )
    except ValueError as exc:
        logger.exception("Payment processing failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "payment_type": request.payment_type,
        "amount": request.amount,
        "currency": request.currency,
        "message": result,
    }


@app.get("/health")
def health() -> dict[str, str]:
    logger.info("Health check called")
    return {"status": "ok"}
