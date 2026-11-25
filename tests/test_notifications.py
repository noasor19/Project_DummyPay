from datetime import datetime
import re

import pytest
from playwright.sync_api import expect

from pages.notifications_page import NotificationsPage

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
def test_notif_06_redirect_without_login(page):
    notifications_page = NotificationsPage(page)
    notifications_page.open()

    expect(page).to_have_url(
        re.compile(r"/login(?:\?.*)?$")
    )
    expect(
        page.get_by_role("button", name="Sign in", exact=True)
    ).to_be_visible()