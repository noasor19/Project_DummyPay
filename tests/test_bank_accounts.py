from uuid import uuid4

import pytest
from playwright.sync_api import expect

from pages.bank_accounts_page import BankAccountsPage
from utilities.test_data import VALID_BANK_ACCOUNT

from utilities.test_data import (
    VALID_BANK_ACCOUNT,
    EMPTY_BANK_ACCOUNT_MESSAGES,
)
from utilities.test_data import (
    INVALID_BANK_ACCOUNT_LETTERS,
    INVALID_BANK_ACCOUNT_LETTERS_MESSAGE,
)
from utilities.test_data import (
    SHORT_BANK_ACCOUNT_NUMBER,
    LONG_BANK_ACCOUNT_NUMBER,
    INVALID_BANK_ACCOUNT_LENGTH_MESSAGE,
)

@pytest.mark.regression
def test_bank_01_add_valid_account(logged_in_page_b):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_name = f"Test Bank {uuid4().hex[:8]}"

    bank_page.open()

    try:
        bank_page.open_add_account_form()
        bank_page.fill_account_details(
            holder_name=VALID_BANK_ACCOUNT["holder_name"],
            bank_name=bank_name,
            country=VALID_BANK_ACCOUNT["country"],
            currency=VALID_BANK_ACCOUNT["currency"],
            account_number=VALID_BANK_ACCOUNT["account_number"],
        )
        bank_page.submit_account()

        expect(bank_page.account_dialog).not_to_be_visible()
        expect(bank_page.get_account(bank_name)).to_have_count(1)

    finally:
        if bank_page.account_dialog.is_visible():
            bank_page.account_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

        if bank_page.get_account(bank_name).count() == 1:
            bank_page.remove_account(bank_name)
            expect(bank_page.get_account(bank_name)).to_have_count(0)

@pytest.mark.regression
def test_bank_02_account_details_are_displayed(logged_in_page_b):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_name = f"Test Bank {uuid4().hex[:8]}"
    account_number = VALID_BANK_ACCOUNT["account_number"]

    bank_page.open()

    try:
        bank_page.open_add_account_form()
        bank_page.fill_account_details(
            holder_name=VALID_BANK_ACCOUNT["holder_name"],
            bank_name=bank_name,
            country=VALID_BANK_ACCOUNT["country"],
            currency=VALID_BANK_ACCOUNT["currency"],
            account_number=account_number,
        )
        bank_page.submit_account()

        expect(bank_page.account_dialog).not_to_be_visible()

        account = bank_page.get_account(bank_name)
        expect(account).to_have_count(1)

        expect(account).to_contain_text(bank_name)

        expect(
            account.get_by_text(
                f"Account •••• {account_number[-4:]}",
                exact=True,
            )
        ).to_be_visible()

        expect(account).not_to_contain_text(account_number)

    finally:
        if bank_page.account_dialog.is_visible():
            bank_page.account_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

        if bank_page.get_account(bank_name).count() == 1:
            bank_page.remove_account(bank_name)
            expect(bank_page.get_account(bank_name)).to_have_count(0)

@pytest.mark.regression
def test_bank_03_remove_account(logged_in_page_b):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_name = f"Test Bank {uuid4().hex[:8]}"

    bank_page.open()

    try:
        bank_page.open_add_account_form()
        bank_page.fill_account_details(
            holder_name=VALID_BANK_ACCOUNT["holder_name"],
            bank_name=bank_name,
            country=VALID_BANK_ACCOUNT["country"],
            currency=VALID_BANK_ACCOUNT["currency"],
            account_number=VALID_BANK_ACCOUNT["account_number"],
        )
        bank_page.submit_account()

        expect(bank_page.account_dialog).not_to_be_visible()
        expect(bank_page.get_account(bank_name)).to_have_count(1)

        bank_page.remove_account(bank_name)

        expect(bank_page.get_account(bank_name)).to_have_count(0)

    finally:
        if bank_page.account_dialog.is_visible():
            bank_page.account_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

        if bank_page.get_account(bank_name).count() == 1:
            bank_page.remove_account(bank_name)
            expect(bank_page.get_account(bank_name)).to_have_count(0)

@pytest.mark.regression
def test_bank_04_empty_required_fields(logged_in_page_b):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_page.open()
    bank_page.open_add_account_form()

    bank_page.submit_account()

    expect(bank_page.account_dialog).to_be_visible()

    for message in EMPTY_BANK_ACCOUNT_MESSAGES:
        expect(
            bank_page.account_dialog.get_by_text(
                message, exact=True
            )
        ).to_be_visible()

@pytest.mark.regression
def test_bank_05_account_number_with_letters(logged_in_page_b):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_name = f"Test Bank {uuid4().hex[:8]}"

    bank_page.open()

    try:
        bank_page.open_add_account_form()
        bank_page.fill_account_details(
            holder_name=VALID_BANK_ACCOUNT["holder_name"],
            bank_name=bank_name,
            country=VALID_BANK_ACCOUNT["country"],
            currency=VALID_BANK_ACCOUNT["currency"],
            account_number=INVALID_BANK_ACCOUNT_LETTERS,
        )
        bank_page.submit_account()

        expect(bank_page.account_dialog).to_be_visible()
        expect(
            bank_page.account_dialog.get_by_text(
                INVALID_BANK_ACCOUNT_LETTERS_MESSAGE,
                exact=True,
            )
        ).to_be_visible()

        bank_page.account_dialog.get_by_role(
            "button", name="Cancel", exact=True
        ).click()

        expect(bank_page.account_dialog).not_to_be_visible()
        expect(bank_page.get_account(bank_name)).to_have_count(0)

    finally:
        if bank_page.account_dialog.is_visible():
            bank_page.account_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

        if bank_page.get_account(bank_name).count() == 1:
            bank_page.remove_account(bank_name)
            expect(bank_page.get_account(bank_name)).to_have_count(0)

@pytest.mark.regression
@pytest.mark.parametrize(
    "account_number",
    [
        SHORT_BANK_ACCOUNT_NUMBER,
        LONG_BANK_ACCOUNT_NUMBER,
    ],
    ids=["too_short", "too_long"],
)
def test_bank_06_invalid_account_length(
    logged_in_page_b, account_number
):
    bank_page = BankAccountsPage(logged_in_page_b)
    bank_name = f"Test Bank {uuid4().hex[:8]}"

    bank_page.open()

    try:
        bank_page.open_add_account_form()
        bank_page.fill_account_details(
            holder_name=VALID_BANK_ACCOUNT["holder_name"],
            bank_name=bank_name,
            country=VALID_BANK_ACCOUNT["country"],
            currency=VALID_BANK_ACCOUNT["currency"],
            account_number=account_number,
        )
        bank_page.submit_account()

        expect(bank_page.account_dialog).to_be_visible()
        expect(
            bank_page.account_dialog.get_by_text(
                INVALID_BANK_ACCOUNT_LENGTH_MESSAGE,
                exact=True,
            )
        ).to_be_visible()

        bank_page.account_dialog.get_by_role(
            "button", name="Cancel", exact=True
        ).click()

        expect(bank_page.account_dialog).not_to_be_visible()
        expect(bank_page.get_account(bank_name)).to_have_count(0)

    finally:
        if bank_page.account_dialog.is_visible():
            bank_page.account_dialog.get_by_role(
                "button", name="Cancel", exact=True
            ).click()

        if bank_page.get_account(bank_name).count() == 1:
            bank_page.remove_account(bank_name)
            expect(bank_page.get_account(bank_name)).to_have_count(0)