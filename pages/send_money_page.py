import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class SendMoneyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = page.get_by_role(
            "heading", name="Send Money", exact=True
        )
        self.recipient_email = page.get_by_label(
            "Recipient's email", exact=True
        )
        self.find_recipient_button = page.get_by_role(
            "button", name="Find recipient", exact=True
        )
        self.continue_button = page.get_by_role(
            "button", name="Continue", exact=True
        )
        self.send_from = page.get_by_label("Send from", exact=True)

        self.amount = page.get_by_label(
    re.compile(r"^Amount to send \(")
)

        self.review_transfer_button = page.get_by_role(
            "button", name="Review transfer", exact=True
        )
        self.confirm_send_button = page.get_by_role(
            "button", name="Confirm & send", exact=True
        )
        self.send_now_button = page.get_by_role(
            "button", name="Send now", exact=True
        )
        self.transfer_complete = page.get_by_role(
            "heading", name="Transfer complete", exact=True
        )

    def open(self):
        super().open("/send")

    def find_recipient(self, email: str):
        self.recipient_email.fill(email)
        self.find_recipient_button.click()

    def continue_to_amount(self):
        self.continue_button.click()

    def select_wallet(self, currency: str):
        self.send_from.click()
        self.page.get_by_role(
        "option",
        name=re.compile(rf"^{re.escape(currency)} wallet"),
        ).click()

    def fill_amount(self, amount: str):
        self.amount.fill(amount)

    def review_transfer(self):
        self.review_transfer_button.click()

    def confirm_and_send(self):
        self.confirm_send_button.click()

    def send_now(self):
        self.send_now_button.click()

    def send_money(self, recipient_email: str, currency: str, amount: str):
        self.open()
        self.find_recipient(recipient_email)
        self.continue_to_amount()
        self.select_wallet(currency)
        self.fill_amount(amount)
        self.review_transfer()
        self.confirm_and_send()
        self.send_now()

    def get_transaction_id(self):
        transaction_text = self.page.get_by_text(
        re.compile(r"^Transaction ID:")
        ).inner_text()

        return transaction_text.split("Transaction ID:", 1)[1].strip()

    def get_received_amount(self):
        summary = self.page.get_by_text(
        re.compile(r"^You sent .+ They received ")
        ).inner_text()

        return summary.split("They received ", 1)[1].removesuffix(".")