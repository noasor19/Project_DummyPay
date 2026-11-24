import re

import pytest
from playwright.sync_api import Page, expect

from pages.forgot_password_page import ForgotPasswordPage
from utilities.config import USER_A_EMAIL


@pytest.mark.regression
def test_fp_01_registered_email(page: Page):
    """TC-FP-01: Reset request for a registered email shows a confirmation"""
    fp_page = ForgotPasswordPage(page)
    fp_page.open()
    fp_page.send_reset_link(USER_A_EMAIL)
    expect(fp_page.success_message(USER_A_EMAIL)).to_be_visible()


@pytest.mark.regression
def test_fp_02_back_to_sign_in(page: Page):
    """TC-FP-02: Back to sign in returns to the Login page"""
    fp_page = ForgotPasswordPage(page)
    fp_page.open()
    fp_page.back_to_sign_in_link.click()
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.regression
def test_fp_04_unregistered_email(page: Page):
    """TC-FP-04: Unregistered email shows the same confirmation"""
    fp_page = ForgotPasswordPage(page)
    fp_page.open()
    fp_page.send_reset_link("notexist123@test.com")
    expect(fp_page.success_message("notexist123@test.com")).to_be_visible()


@pytest.mark.regression
def test_fp_05_empty_email(page: Page):
    """TC-FP-05: Empty email shows an error"""
    fp_page = ForgotPasswordPage(page)
    fp_page.open()
    fp_page.send_reset_link_button.click()
    expect(fp_page.email_error).to_be_visible()
    expect(page).to_have_url(re.compile(r"/forgot-password$"))


@pytest.mark.regression
def test_fp_06_invalid_email_format(page: Page):
    """TC-FP-06: Email without @ shows a format error"""
    fp_page = ForgotPasswordPage(page)
    fp_page.open()
    fp_page.send_reset_link("userexample.com")
    expect(fp_page.email_error).to_be_visible()
    expect(page).to_have_url(re.compile(r"/forgot-password$"))