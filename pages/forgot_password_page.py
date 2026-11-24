from playwright.sync_api import Page

from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email = page.get_by_label("Email", exact=True)
        self.send_reset_link_button = page.get_by_role("button", name="Send reset link", exact=True)
        self.back_to_sign_in_link = page.get_by_role("link", name="Back to sign in", exact=True)
        self.email_error = page.get_by_text("Enter a valid email address.", exact=True)

    def open(self):
        super().open("/forgot-password")

    def send_reset_link(self, email: str):
        self.email.fill(email)
        self.send_reset_link_button.click()

    def success_message(self, email: str):
        return self.page.get_by_text(f"If an account exists for {email}")

    








    