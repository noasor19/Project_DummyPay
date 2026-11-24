import pytest
from playwright.sync_api import expect

from pages.payment_cards_page import PaymentCardsPage
from utilities.test_data import VALID_CARD
from uuid import uuid4
from utilities.test_data import (
    VALID_CARD,
    INVALID_CARD_NUMBER,
    INVALID_CARD_NUMBER_MESSAGE,
)
from utilities.test_data import (
    EXPIRED_CARD_DATE,
    EXPIRED_CARD_MESSAGE,
)
from utilities.test_data import (
    INVALID_CVV,
    INVALID_CVV_MESSAGE,
)
from utilities.test_data import EMPTY_CARD_MESSAGES

@pytest.mark.smoke
@pytest.mark.regression
def test_card_01_add_valid_card(logged_in_page_b):
    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"
    
    cards_page.open_add_card_form()
    expect(cards_page.card_dialog).to_be_visible()

    cards_page.fill_card_details(
        name=card_name,
        number=VALID_CARD["number"],
        expiry=VALID_CARD["expiry"],
        cvv=VALID_CARD["cvv"],
    )
    cards_page.submit_card()

    try:
        expect(cards_page.card_dialog).not_to_be_visible()
        expect(cards_page.get_card(card_name)).to_be_visible()
    finally:
        card = cards_page.get_card(card_name)
        if card.count() == 1:
            cards_page.remove_card(card_name)
            expect(card).to_have_count(0)

@pytest.mark.regression
def test_card_02_card_number_is_masked(logged_in_page_b):
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"

    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()

    cards_page.fill_card_details(
        name=card_name,
        number=VALID_CARD["number"],
        expiry=VALID_CARD["expiry"],
        cvv=VALID_CARD["cvv"],
    )

    try:
        cards_page.submit_card()
        expect(cards_page.card_dialog).not_to_be_visible()

        card = cards_page.get_card(card_name)
        expect(card).to_be_visible()

        masked_number = "•••• •••• •••• 1111"
        expect(
            card.get_by_text(masked_number, exact=True)
        ).to_be_visible()
        expect(card).not_to_contain_text(VALID_CARD["number"])
        expect(card).not_to_contain_text("4111 1111 1111 1111")
    finally:
        card = cards_page.get_card(card_name)
        if card.count() == 1:
            cards_page.remove_card(card_name)
            expect(card).to_have_count(0)

@pytest.mark.regression
def test_card_03_remove_card(logged_in_page_b):
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"

    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()

    cards_page.fill_card_details(
        name=card_name,
        number=VALID_CARD["number"],
        expiry=VALID_CARD["expiry"],
        cvv=VALID_CARD["cvv"],
    )

    try:
        cards_page.submit_card()
        expect(cards_page.card_dialog).not_to_be_visible()

        card = cards_page.get_card(card_name)
        expect(card).to_be_visible()

        cards_page.remove_card(card_name)
        expect(card).to_have_count(0)

        logged_in_page_b.reload()
        expect(
            logged_in_page_b.get_by_role(
                "heading", name="Payment Cards", exact=True
            )
        ).to_be_visible()
        expect(cards_page.get_card(card_name)).to_have_count(0)
    finally:
        card = cards_page.get_card(card_name)
        if card.count() == 1:
            cards_page.remove_card(card_name)
            expect(card).to_have_count(0)

@pytest.mark.regression
def test_card_04_invalid_card_number(logged_in_page_b):
    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"
    cards_page.fill_card_details(
        name=card_name,
        number=INVALID_CARD_NUMBER,
        expiry=VALID_CARD["expiry"],
        cvv=VALID_CARD["cvv"],
    )
    cards_page.submit_card()

    expect(cards_page.card_dialog).to_be_visible()
    expect(
        cards_page.card_dialog.get_by_text(
            INVALID_CARD_NUMBER_MESSAGE, exact=True
        )
    ).to_be_visible()

    cards_page.card_dialog.get_by_role(
        "button", name="Cancel", exact=True
    ).click()

    expect(cards_page.card_dialog).not_to_be_visible()
    expect(cards_page.get_card(card_name)).to_have_count(0)

@pytest.mark.regression
def test_card_05_expired_card(logged_in_page_b):
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"

    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()

    cards_page.fill_card_details(
        name=card_name,
        number=VALID_CARD["number"],
        expiry=EXPIRED_CARD_DATE,
        cvv=VALID_CARD["cvv"],
    )
    cards_page.submit_card()

    expect(
        cards_page.card_dialog.get_by_text(
            EXPIRED_CARD_MESSAGE, exact=True
        )
    ).to_be_visible()

    cards_page.card_dialog.get_by_role(
        "button", name="Cancel", exact=True
    ).click()

    expect(cards_page.card_dialog).not_to_be_visible()
    expect(cards_page.get_card(card_name)).to_have_count(0)

@pytest.mark.regression
def test_card_06_two_digit_cvv(logged_in_page_b):
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"

    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()

    cards_page.fill_card_details(
        name=card_name,
        number=VALID_CARD["number"],
        expiry=VALID_CARD["expiry"],
        cvv=INVALID_CVV,
    )
    cards_page.submit_card()

    expect(
        cards_page.card_dialog.get_by_text(
            INVALID_CVV_MESSAGE, exact=True
        )
    ).to_be_visible()

    cards_page.card_dialog.get_by_role(
        "button", name="Cancel", exact=True
    ).click()

    expect(cards_page.card_dialog).not_to_be_visible()
    expect(cards_page.get_card(card_name)).to_have_count(0)

@pytest.mark.regression
def test_card_07_empty_fields(logged_in_page_b):
    cards_page = PaymentCardsPage(logged_in_page_b)
    cards_page.open()
    cards_page.open_add_card_form()
    cards_page.submit_card()

    expect(cards_page.card_dialog).to_be_visible()

    for message in EMPTY_CARD_MESSAGES:
        expect(
            cards_page.card_dialog.get_by_text(
                message, exact=True
            )
        ).to_be_visible()

@pytest.mark.xfail(reason="BUG-001 | Able to add duplicate card")
@pytest.mark.regression
def test_card_08_duplicate_card_is_rejected(logged_in_page_b):
    suffix = uuid4().hex[:8].translate(
        str.maketrans("0123456789", "abcdefghij")
    )
    card_name = f"Test {suffix}"

    page = logged_in_page_b
    cards_page = PaymentCardsPage(page)
    cards_page.open()

    try:
        cards_page.open_add_card_form()
        cards_page.fill_card_details(
            name=card_name,
            number=VALID_CARD["number"],
            expiry=VALID_CARD["expiry"],
            cvv=VALID_CARD["cvv"],
        )
        cards_page.submit_card()

        expect(cards_page.card_dialog).not_to_be_visible()
        expect(cards_page.get_card(card_name)).to_have_count(1)

        cards_page.open_add_card_form()
        cards_page.fill_card_details(
            name=card_name,
            number=VALID_CARD["number"],
            expiry=VALID_CARD["expiry"],
            cvv=VALID_CARD["cvv"],
        )

        with page.expect_response(
            lambda response:
                "/functions/v1/add-payment-card" in response.url
                and response.request.method == "POST"
        ) as save_response:
            cards_page.submit_card()

        response = save_response.value
        response.finished()

        if response.status == 201:
            expect(cards_page.card_dialog).not_to_be_visible()
            expect(cards_page.get_card(card_name)).to_have_count(2)

        assert 400 <= response.status < 500, (
            "Expected duplicate card rejection, "
            f"but received HTTP {response.status}"
        )

        expect(cards_page.card_dialog).to_be_visible()

        cards_page.card_dialog.get_by_role(
            "button", name="Cancel", exact=True
        ).click()

        expect(cards_page.card_dialog).not_to_be_visible()
        expect(cards_page.get_card(card_name)).to_have_count(1)

    finally:
        if cards_page.card_dialog.is_visible():
            cards_page.card_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

            expect(cards_page.card_dialog).not_to_be_visible()

        cards = cards_page.get_card(card_name)

        while cards.count() > 0:
            count_before = cards.count()

            cards.first.get_by_role(
                "button", name="Remove card ending in"
            ).click()
            cards_page.confirm_card_removal()

            expect(cards).to_have_count(count_before - 1)