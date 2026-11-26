import re

import pytest
from playwright.sync_api import expect

from pages.send_money_page import SendMoneyPage
from pages.wallets_page import WalletsPage
from utilities.config import USER_A_EMAIL, USER_B_EMAIL


def go_to_amount_step(send_page: SendMoneyPage):
    send_page.open()
    send_page.find_recipient(USER_B_EMAIL)
    send_page.continue_to_amount()


def to_minor(amount_text: str) -> int:
    # "£2.38" -> 238
    return round(float(amount_text[1:].replace(",", "")) * 100)


# ---------- B's test ----------

@pytest.mark.smoke
@pytest.mark.regression
def test_send_money_successfully(logged_in_page_b):
    send_page = SendMoneyPage(logged_in_page_b)

    send_page.send_money(
        recipient_email=USER_A_EMAIL,
        currency="ILS",
        amount="1.00",
    )

    expect(send_page.transfer_complete).to_be_visible()


# ---------- positive tests ----------

@pytest.mark.regression
def test_send_02_recipient_receives_money(logged_in_users):
    """TC-SEND-02: The recipient's balance grows by the converted amount"""
    page_a, page_b = logged_in_users
    wallets_b = WalletsPage(page_b)
    wallets_b.open()
    gbp_balance = page_b.get_by_text(re.compile(r"^£"))
    text_before = gbp_balance.inner_text()

    send_page = SendMoneyPage(page_a)
    send_page.send_money(recipient_email=USER_B_EMAIL, currency="ILS", amount="1.00")
    expect(send_page.transfer_complete).to_be_visible()
    received = to_minor(send_page.get_received_amount())

    wallets_b.open()
    expect(gbp_balance).not_to_have_text(text_before)
    assert to_minor(gbp_balance.inner_text()) - to_minor(text_before) == received


@pytest.mark.regression
def test_send_03_decimal_amount(logged_in_page_a):
    """TC-SEND-03: A decimal amount (10.50) is sent successfully"""
    send_page = SendMoneyPage(logged_in_page_a)
    send_page.send_money(recipient_email=USER_B_EMAIL, currency="ILS", amount="10.50")
    expect(send_page.transfer_complete).to_be_visible()
    expect(logged_in_page_a.get_by_text("You sent ₪10.50", exact=False)).to_be_visible()


# ---------- negative ----------

@pytest.mark.regression
def test_send_04_zero_amount(logged_in_page_a):
    """TC-SEND-04: Amount 0 shows an error and does not continue"""
    send_page = SendMoneyPage(logged_in_page_a)
    go_to_amount_step(send_page)
    send_page.fill_amount("0")
    send_page.review_transfer()
    expect(logged_in_page_a.get_by_text("Amount must be greater than zero.", exact=True)).to_be_visible()
    expect(send_page.confirm_send_button).not_to_be_visible()


@pytest.mark.regression
def test_send_05_negative_amount(logged_in_page_a):
    """TC-SEND-05: Negative amount shows an error and does not continue"""
    send_page = SendMoneyPage(logged_in_page_a)
    go_to_amount_step(send_page)
    send_page.fill_amount("-10")
    send_page.review_transfer()
    expect(logged_in_page_a.get_by_text("Enter a valid positive number.", exact=True)).to_be_visible()
    expect(send_page.confirm_send_button).not_to_be_visible()


@pytest.mark.regression
def test_send_06_amount_above_balance(logged_in_page_a):
    """TC-SEND-06: Amount above the balance shows an error and does not continue"""
    send_page = SendMoneyPage(logged_in_page_a)
    go_to_amount_step(send_page)
    send_page.fill_amount("999999")
    send_page.review_transfer()
    expect(logged_in_page_a.get_by_text(re.compile(r"^You only have .+ available\.$"))).to_be_visible()
    expect(send_page.confirm_send_button).not_to_be_visible()


@pytest.mark.regression
def test_send_07_unregistered_recipient(logged_in_page_a):
    """TC-SEND-07: An unregistered email shows an error"""
    send_page = SendMoneyPage(logged_in_page_a)
    send_page.open()
    send_page.find_recipient("notexist123@test.com")
    expect(logged_in_page_a.get_by_text("No registered user found with this email address.", exact=True)).to_be_visible()
    expect(send_page.continue_button).not_to_be_visible()


@pytest.mark.regression
def test_send_08_send_to_self(logged_in_page_a):
    """TC-SEND-08: Sending to your own email shows an error"""
    send_page = SendMoneyPage(logged_in_page_a)
    send_page.open()
    send_page.find_recipient(USER_A_EMAIL)
    expect(logged_in_page_a.get_by_text("You cannot send money to yourself.", exact=True)).to_be_visible()
    expect(send_page.continue_button).not_to_be_visible()
