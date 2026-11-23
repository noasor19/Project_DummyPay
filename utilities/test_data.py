VALID_CARD = {
    "name": "Chaya Turner",
    "number": "4111111111111111",
    "expiry": "03/30",
    "cvv": "737",
}

INVALID_CARD_NUMBER = "4111111111111112"

INVALID_CARD_NUMBER_MESSAGE = (
    "Card number is not valid (checksum failed)."
)

EXPIRED_CARD_DATE = "01/20"
EXPIRED_CARD_MESSAGE = "This card has expired."

INVALID_CVV = "73"
INVALID_CVV_MESSAGE = "CVV must be 3 digits."

EMPTY_CARD_MESSAGES = [
    "Cardholder name must be 2–100 characters.",
    "Card number may only contain digits.",
    "Expiry must be in MM/YY format.",
    "CVV must be 3 digits.",
]