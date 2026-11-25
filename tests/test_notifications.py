import pytest
from playwright.sync_api import expect
from datetime import datetime, timezone
import re
from decimal import Decimal
from pages.notifications_page import NotificationsPage
from pages.send_money_page import SendMoneyPage
from utilities.config import USER_A_EMAIL, USER_B_EMAIL

@pytest.mark.browser_context_args(locale="en-GB", timezone_id="UTC")
@pytest.mark.regression
def test_notif_01_payment_received(logged_in_users):
    page_a, page_b = logged_in_users

    notifications_page = NotificationsPage(page_b)
    notifications_page.open()

    # מוודאים שהרשימה הקיימת נטענה
    expect(notifications_page.notifications.first).to_be_visible()
    count_before = notifications_page.notifications.count()

    send_page = SendMoneyPage(page_a)
    started_at = datetime.now(timezone.utc).replace(
    second=0, microsecond=0
    )
    send_page.send_money(
        recipient_email=USER_B_EMAIL,
        currency="ILS",
        amount="1.00",
    )

    expect(send_page.transfer_complete).to_be_visible()
    received_amount = send_page.get_received_amount()
    notifications_page.open()

    expect(notifications_page.notifications).to_have_count(
        count_before + 1
    )

    new_notification = notifications_page.notifications.first

    expect(new_notification).to_contain_text("Payment received")
    expect(new_notification).to_contain_text(USER_A_EMAIL)
    expect(new_notification).to_have_attribute("data-read", "false")
    expect(new_notification).to_contain_text(
    f"sent you {received_amount}."
    )
    date_text = new_notification.locator("span.text-xs").inner_text()

    notification_time = datetime.strptime(
    " ".join(date_text.split()),
    "%d %b %Y, %H:%M",
    ).replace(tzinfo=timezone.utc)

    assert started_at <= notification_time <= datetime.now(timezone.utc), (
    "Notification time does not match the transfer time"
    )

@pytest.mark.regression
def test_notif_02_mark_notification_as_read(logged_in_users):
    page_a, page_b = logged_in_users

    notifications_page = NotificationsPage(page_b)
    notifications_page.open()

    expect(notifications_page.notifications.first).to_be_visible()
    count_before = notifications_page.notifications.count()

    send_page = SendMoneyPage(page_a)
    send_page.send_money(
        recipient_email=USER_B_EMAIL,
        currency="ILS",
        amount="1.00",
    )
    expect(send_page.transfer_complete).to_be_visible()

    notifications_page.open()
    expect(notifications_page.notifications).to_have_count(
        count_before + 1
    )

    notification = notifications_page.notifications.first
    expect(notification).to_have_attribute("data-read", "false")

    unread_before = notifications_page.notifications.filter(
        has=page_b.get_by_role(
            "button", name="Mark read", exact=True
        )
    ).count()

    notification.get_by_role(
        "button", name="Mark read", exact=True
    ).click()

    expect(notification).to_have_attribute("data-read", "true")
    expect(
        notification.get_by_role(
            "button", name="Mark read", exact=True
        )
    ).not_to_be_visible()

    expect(notifications_page.unread_tab).to_have_text(
        f"Unread ({unread_before - 1})"
    )

    notifications_page.unread_tab.click()

    expect(notifications_page.notifications).to_have_count(
        unread_before - 1
    )
    expect(
    notifications_page.notifications.locator(
        'xpath=self::*[@data-read="true"]'
    )
    ).to_have_count(0)

    
@pytest.mark.browser_context_args(locale="en-US")
@pytest.mark.regression
def test_notif_03_notifications_order(logged_in_page_b):
    notifications_page = NotificationsPage(logged_in_page_b)
    notifications_page.open()

    expect(notifications_page.notifications.nth(1)).to_be_visible()

    date_texts = notifications_page.get_notification_dates()
    dates = [
    datetime.strptime(
        " ".join(text.split()),
        "%b %d, %Y, %I:%M %p",
    )
    for text in date_texts
]

    assert dates == sorted(dates, reverse=True), (
        "Notifications are not ordered from newest to oldest"
    )

@pytest.mark.regression
def test_notif_05_failed_transfer_creates_no_notification(
    logged_in_users,
):
    page_a, page_b = logged_in_users

    notifications_page = NotificationsPage(page_b)
    notifications_page.open()

    expect(notifications_page.notifications.first).to_be_visible()
    notifications_before = (
        notifications_page.notifications.all_text_contents()
    )

    send_page = SendMoneyPage(page_a)
    send_page.open()
    send_page.find_recipient(USER_B_EMAIL)
    send_page.continue_to_amount()
    send_page.select_wallet("ILS")

    wallet_text = send_page.send_from.inner_text()
    balance_match = re.search(r"[\d,]+\.\d{2}", wallet_text)
    assert balance_match, "Wallet balance was not found"

    balance = Decimal(balance_match.group().replace(",", ""))
    send_page.fill_amount(str(balance + Decimal("1.00")))
    send_page.review_transfer()

    expect(
        page_a.get_by_text(
            re.compile(r"^You only have .+ available\.$")
        )
    ).to_be_visible()

    notifications_page.open()

    expect(notifications_page.notifications).to_have_text(
        notifications_before
    )

@pytest.mark.regression
def test_notif_06_redirect_without_login(page):
    notifications_page = NotificationsPage(page)
    notifications_page.open()

    expect(page).to_have_url(
        re.compile(r"/login(?:\?.*)?$")
    )
    expect(
        page.get_by_role("button", name="Sign in", exact=True)
    ).to_be_visible()