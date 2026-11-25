import re

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard_page import DashboardPage
from utilities.config import BASE_URL

MENU_PAGES = [
    "Wallets",
    "Send Money",
    "Transaction History",
    "Payment Cards",
    "Bank Accounts",
    "Notifications",
    "Profile & Settings",
    "Dashboard",
]


@pytest.mark.smoke
@pytest.mark.regression
def test_dash_01_dashboard_loads(logged_in_page_a):
    """TC-DASH-01: Dashboard shows heading, welcome message, total balance and menu"""
    dashboard = DashboardPage(logged_in_page_a)
    expect(dashboard.heading).to_be_visible()
    expect(dashboard.welcome_message).to_be_visible()
    expect(dashboard.total_balance).to_be_visible()
    expect(dashboard.menu).to_be_visible()


@pytest.mark.regression
def test_dash_02_menu_navigation(logged_in_page_a):
    """TC-DASH-02: Each menu link opens the page with the matching heading"""
    dashboard = DashboardPage(logged_in_page_a)
    for page_name in MENU_PAGES:
        dashboard.go_to(page_name)
        expect(logged_in_page_a.get_by_role("heading", level=1)).to_have_text(page_name)


@pytest.mark.regression
def test_dash_03_balance_matches_wallets(logged_in_page_a):
    """TC-DASH-03: Total balance on Dashboard equals Total balance on Wallets"""
    dashboard = DashboardPage(logged_in_page_a)
    dashboard_balance = dashboard.total_balance.inner_text()
    dashboard.go_to("Wallets")
    expect(logged_in_page_a.get_by_text(re.compile(r"^≈")).first).to_have_text(dashboard_balance)


@pytest.mark.regression
def test_dash_04_no_access_without_login(page: Page):
    """TC-DASH-04: Opening the Dashboard without login redirects to Login"""
    dashboard = DashboardPage(page)
    dashboard.open()
    expect(page).to_have_url(re.compile(r"/login$"))


@pytest.mark.regression
def test_dash_05_back_after_sign_out(logged_in_page_a):
    """TC-DASH-05: Back after sign out does not show the Dashboard"""
    dashboard = DashboardPage(logged_in_page_a)
    dashboard.sign_out()
    expect(logged_in_page_a).to_have_url(re.compile(r"/login$"))
    logged_in_page_a.go_back()
    expect(dashboard.heading).not_to_be_visible()


@pytest.mark.regression
def test_dash_06_unknown_page_redirects(logged_in_page_a):
    """TC-DASH-06: An unknown address redirects to the Dashboard"""
    logged_in_page_a.goto(f"{BASE_URL}/dashboard123")
    dashboard = DashboardPage(logged_in_page_a)
    expect(dashboard.heading).to_be_visible()
    expect(logged_in_page_a).to_have_url(re.compile(r"vercel\.app/$"))