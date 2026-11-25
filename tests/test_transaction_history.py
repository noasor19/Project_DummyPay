import re
from decimal import Decimal
import pytest
from playwright.sync_api import expect

from pages.send_money_page import SendMoneyPage
from pages.transaction_history_page import TransactionHistoryPage
from utilities.config import USER_A_EMAIL, USER_B_EMAIL
from pages.login_page import LoginPage
from utilities.config import USER_B_PASSWORD
from datetime import date, timedelta
from utilities.test_data import (
    INVALID_HISTORY_DATE,
    HISTORY_LOAD_ERROR_MESSAGE,
)

@pytest.mark.regression
def test_trx_01_new_outgoing_transaction(logged_in_page_b):
    send_page = SendMoneyPage(logged_in_page_b)
    send_page.send_money(
        recipient_email=USER_A_EMAIL,
        currency="ILS",
        amount="1.00",
    )

    expect(send_page.transfer_complete).to_be_visible()
    transaction_id = send_page.get_transaction_id()
    assert transaction_id, "Transaction ID is missing"

    history_page = TransactionHistoryPage(logged_in_page_b)
    history_page.open()

    expect(history_page.heading).to_be_visible()
    expect(history_page.transactions.first).to_contain_text("Sent")
    expect(history_page.transactions.first).to_contain_text("1.00")

    history_page.open_first_transaction()

    dialog = history_page.transaction_dialog
    expect(dialog).to_be_visible()
    expect(
        dialog.get_by_text(transaction_id, exact=True)
    ).to_be_visible()
    expect(
        dialog.get_by_text(USER_B_EMAIL, exact=True)
    ).to_be_visible()
    expect(
        dialog.get_by_text(USER_A_EMAIL, exact=True)
    ).to_be_visible()
    expect(
        dialog.get_by_text("Sent", exact=True)
    ).to_be_visible()
    expect(
        dialog.get_by_text("completed", exact=True)
    ).to_be_visible()

@pytest.mark.regression
def test_trx_02_new_incoming_transaction(
    logged_in_page_a, browser
):
    send_page = SendMoneyPage(logged_in_page_a)
    send_page.send_money(
        recipient_email=USER_B_EMAIL,
        currency="ILS",
        amount="1.00",
    )

    expect(send_page.transfer_complete).to_be_visible()
    transaction_id = send_page.get_transaction_id()

    context_b = browser.new_context()
    page_b = context_b.new_page()

    try:
        login_page = LoginPage(page_b)
        login_page.open()
        login_page.login(USER_B_EMAIL, USER_B_PASSWORD)

        expect(
            page_b.get_by_role(
                "heading", name="Dashboard", exact=True
            )
        ).to_be_visible()

        history_page = TransactionHistoryPage(page_b)
        history_page.open()
        expect(history_page.heading).to_be_visible()

        expect(
            history_page.transactions.first
        ).to_contain_text("Received")

        history_page.open_first_transaction()

        dialog = history_page.transaction_dialog
        expect(dialog).to_be_visible()
        expect(
            dialog.get_by_text(transaction_id, exact=True)
        ).to_be_visible()
        expect(
            dialog.get_by_text(USER_A_EMAIL, exact=True)
        ).to_be_visible()
        expect(
            dialog.get_by_text(USER_B_EMAIL, exact=True)
        ).to_be_visible()
        expect(
            dialog.get_by_text("Received", exact=True)
        ).to_be_visible()

    finally:
        context_b.close()

@pytest.mark.regression
def test_trx_03_filter_sent_transactions(logged_in_page_b):
    history_page = TransactionHistoryPage(logged_in_page_b)
    history_page.open()

    sent_transactions = history_page.transactions.filter(
        has_text="Sent"
    )
    received_transactions = history_page.transactions.filter(
        has_text="Received"
    )

    # מוודאים שקיימים שני סוגי העסקאות לפני הסינון
    expect(sent_transactions.first).to_be_visible()
    expect(received_transactions.first).to_be_visible()

    history_page.filter_by_type("Sent")

    expect(history_page.transactions.first).to_be_visible()

    # כל השורות המוצגות חייבות להיות עסקאות יוצאות
    expect(
        history_page.transactions.filter(has_not_text="Sent")
    ).to_have_count(0)

    expect(received_transactions).to_have_count(0)

@pytest.mark.regression
def test_trx_04_future_date_has_no_transactions(logged_in_page_b):
    history_page = TransactionHistoryPage(logged_in_page_b)
    history_page.open()

    expect(history_page.transactions.first).to_be_visible()

    future_date = date.today() + timedelta(days=365)
    history_page.from_date.fill(future_date.isoformat())

    expect(history_page.no_transactions_message).to_be_visible()
    expect(history_page.transactions).to_have_count(0)

@pytest.mark.regression
def test_trx_05_failed_transfer_not_in_history(logged_in_page_b):
    history_page = TransactionHistoryPage(logged_in_page_b)
    history_page.open()

    expect(history_page.transactions.first).to_be_visible()
    transactions_before = history_page.transactions.all_text_contents()

    send_page = SendMoneyPage(logged_in_page_b)
    send_page.open()
    send_page.find_recipient(USER_A_EMAIL)
    send_page.continue_to_amount()
    send_page.select_wallet("ILS")

    wallet_text = send_page.send_from.inner_text()
    balance_match = re.search(r"[\d,]+\.\d{2}", wallet_text)
    assert balance_match, "Wallet balance was not found"

    balance = Decimal(balance_match.group().replace(",", ""))
    excessive_amount = balance + Decimal("1.00")

    send_page.fill_amount(str(excessive_amount))
    send_page.review_transfer()

    expect(
        logged_in_page_b.get_by_text(
            re.compile(r"^You only have .+ available\.$")
        )
    ).to_be_visible()

    expect(send_page.amount).to_be_visible()
    expect(send_page.transfer_complete).not_to_be_visible()

    history_page.open()

    expect(history_page.transactions).to_have_text(
        transactions_before
    )

@pytest.mark.regression
def test_trx_06_invalid_date_shows_error(logged_in_page_b):
    history_page = TransactionHistoryPage(logged_in_page_b)
    history_page.open()

    expect(history_page.transactions.first).to_be_visible()

    history_page.from_date.fill(INVALID_HISTORY_DATE)
    history_page.from_date.press("Tab")

    expect(history_page.from_date).to_have_value(
        INVALID_HISTORY_DATE
    )
    expect(
        logged_in_page_b.get_by_text(
            HISTORY_LOAD_ERROR_MESSAGE, exact=True
        )
    ).to_be_visible()

    expect(history_page.heading).to_be_visible()
    expect(history_page.transactions).to_have_count(0)