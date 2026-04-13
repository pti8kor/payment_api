from typing import Callable

from payments_api.logging_config import get_logger
from payments_api.models.payment import Payment


logger = get_logger(__name__)


class PaymentFactory:
    _creators: dict[str, Callable[..., Payment]] = {}

    @classmethod
    def register_payment(cls, payment_type: str, creator: Callable[..., Payment]) -> None:
        normalized_type = payment_type.strip().lower()
        if not normalized_type:
            raise ValueError("Payment type cannot be empty")
        cls._creators[normalized_type] = creator
        logger.info("Registered payment type '%s'", normalized_type)

    @classmethod
    def create_payment(cls, payment_type: str, amount: float, currency: str, **kwargs) -> Payment:
        normalized_type = payment_type.strip().lower()
        # BREAKPOINT 4a: See the normalized payment type
        creator = cls._creators.get(normalized_type)

        if creator is None:
            supported = ", ".join(sorted(cls._creators)) or "none"
            logger.warning(
                "Unknown payment type '%s'. Supported: %s",
                payment_type,
                supported,
            )
            raise ValueError(
                f"Invalid payment type '{payment_type}'. Supported types: {supported}"
            )

        try:
            # BREAKPOINT 4b: About to call the creator function
            logger.info("Creating payment object | type=%s", normalized_type)
            return creator(amount, currency, **kwargs)
        except TypeError as exc:
            logger.exception("Invalid creator arguments for type '%s': %s", normalized_type, exc)
            raise ValueError(f"Invalid arguments for '{normalized_type}': {exc}") from exc
