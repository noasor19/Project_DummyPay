from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email = page.get_by_label("Email", exact=True)
        self.password = page.get_by_label("Password", exact=True)
        self.sign_in_button = page.get_by_role(
            "button", name="Sign in", exact=True
        )

    def open(self):
        super().open("/login")

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.sign_in_button.click()