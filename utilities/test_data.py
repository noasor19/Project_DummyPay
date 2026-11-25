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
VALID_BANK_ACCOUNT = {
    "holder_name": "Test User",
    "bank_name": "Test Bank",
    "country": "Israel",
    "currency": "ILS",
    "account_number": "123456789",
}

INVALID_BANK_ACCOUNT_LETTERS = "ABCDE"
SHORT_BANK_ACCOUNT_NUMBER = "123"
LONG_BANK_ACCOUNT_NUMBER = "123456789012345678901"

EMPTY_BANK_ACCOUNT_MESSAGES = [
    "Account holder name must be 2–100 characters.",
    "Bank name must be 2–100 characters.",
    "Choose a supported country.",
    "Choose a supported currency.",
    "Enter an IBAN or an account number of 4–20 digits.",
]
INVALID_BANK_ACCOUNT_LETTERS = "ABCD"
INVALID_BANK_ACCOUNT_LETTERS_MESSAGE = "IBAN format is not valid."

INVALID_BANK_ACCOUNT_LENGTH_MESSAGE = (
    "Enter an IBAN or an account number of 4–20 digits."
)

INVALID_DISPLAY_NAME_MESSAGE = (
    "Display name must be at least 2 characters."
)