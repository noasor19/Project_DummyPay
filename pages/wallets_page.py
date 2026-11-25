import re

from playwright.sync_api import Page

from pages.base_page import BasePage


class WalletsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Wallets", exact=True)
        self.total_balance = page.get_by_text(re.compile(r"^≈"))
        self.ils_balance = page.get_by_text(re.compile(r"^₪"))
        self.add_wallet_button = page.get_by_role("button", name="Add wallet", exact=True)
        self.add_wallet_dialog = page.get_by_role("dialog")
        self.currency_select = self.add_wallet_dialog.get_by_role("combobox")
        self.currency_options = page.get_by_role("option")
        self.amount = page.get_by_label("Amount", exact=True)
        self.converted_amount = page.get_by_text(re.compile(r"^\$\d")).last
        self.rate_text = page.get_by_text(re.compile(r"^Rate:"))
        self.amount_error = page.get_by_text("Enter a valid positive number.", exact=True)

    def open(self):
        super().open("/wallets")

    def open_currency_list(self):
        self.add_wallet_button.click()
        self.currency_select.click()

    def get_rate(self) -> float:
        # "Rate: 1 ILS = 0.299419 USD" -> 0.299419
        return float(self.rate_text.inner_text().split("=")[1].split()[0])