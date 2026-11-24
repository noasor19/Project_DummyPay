import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utilities.config import USER_A_EMAIL, USER_A_PASSWORD


#test_login_01_a_and_b
@pytest.mark.smoke
@pytest.mark.regression
def test_login_user_a(logged_in_page_a):
    """TC-LOGIN-01: User A logs in with valid details"""
    expect(
        logged_in_page_a.get_by_role(
            "heading", name="Dashboard", exact=True
        )
    ).to_be_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_login_user_b(logged_in_page_b):
    """TC-LOGIN-01: User B logs in with valid details"""
    expect(
        logged_in_page_b.get_by_role(
            "heading", name="Dashboard", exact=True
        )
    ).to_be_visible()



@pytest.mark.regression
def test_login_02_uppercase_email(page: Page):
    """TC-LOGIN-02: Login with the email written in capital letters"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_A_EMAIL.upper(), USER_A_PASSWORD)
    expect(page.get_by_role("heading", name="Dashboard", exact=True)).to_be_visible()


@pytest.mark.regression
def test_login_03_forgot_password_link(page: Page):
    """TC-LOGIN-03: The Forgot password? link opens the reset page"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.forgot_password_link.click()
    expect(page).to_have_url(re.compile(r"/forgot-password$"))
    expect(page.get_by_text("Reset your password", exact=True)).to_be_visible()


@pytest.mark.regression
def test_login_04_wrong_password(page: Page):
    """TC-LOGIN-04: Wrong password shows an error and stays on Login"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(USER_A_EMAIL, "wrong123")
    expect(login_page.login_error_message).to_be_visible()
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.regression
def test_login_05_unregistered_email(page: Page):
    """TC-LOGIN-05: An email that is not registered cannot log in"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("notexist123@test.com", "wrong123")
    expect(login_page.login_error_message).to_be_visible()
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.regression
def test_login_06_empty_fields(page: Page):
    """TC-LOGIN-06: Empty fields show an error under each field"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.sign_in_button.click()
    expect(login_page.email_error).to_be_visible()
    expect(login_page.password_error).to_be_visible()


@pytest.mark.regression
def test_login_07_invalid_email_format(page: Page):
    """TC-LOGIN-07: An email without @ shows a format error"""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("userexample.com", "anything123")
    expect(login_page.email_error).to_be_visible()
    expect(page).to_have_url(re.compile(r"/login$"))