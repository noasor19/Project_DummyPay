import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Dashboard", exact=True)
        self.welcome_message = page.get_by_text(re.compile(r"^Welcome back"))
        self.total_balance = page.get_by_text(re.compile(r"^≈")).first
        self.menu = page.get_by_role("navigation")
        self.account_menu_button = page.get_by_role("button", name=re.compile("Account menu"))
        self.sign_out_button = page.get_by_role("menuitem", name="Sign out")

    def open(self):
        super().open("/")

    def go_to(self, page_name: str):
        self.menu.get_by_role("link", name=page_name).click()

    def sign_out(self):
        self.account_menu_button.click()
        self.sign_out_button.click()