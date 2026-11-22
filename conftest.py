import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utilities.config import (
    USER_A_EMAIL,
    USER_A_PASSWORD,
    USER_B_EMAIL,
    USER_B_PASSWORD,
)


def login_as(page: Page, email: str, password: str):
    if not email or not password:
        pytest.fail("Set the test user's email and password in .env")

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email, password)

    expect(
        page.get_by_role("heading", name="Dashboard", exact=True)
    ).to_be_visible()

    return page


@pytest.fixture
def logged_in_page_b(page: Page):
    return login_as(page, USER_B_EMAIL, USER_B_PASSWORD)


@pytest.fixture
def logged_in_page_a(page: Page):
    return login_as(page, USER_A_EMAIL, USER_A_PASSWORD)