import pytest
from playwright.sync_api import expect

from pages.send_money_page import SendMoneyPage
from utilities.config import USER_A_EMAIL


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