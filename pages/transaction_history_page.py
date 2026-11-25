from playwright.sync_api import Page

from pages.base_page import BasePage


class TransactionHistoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Transaction History", exact=True
        )
        self.transactions = page.get_by_test_id("transaction-row")
        self.transaction_dialog = page.get_by_role("dialog")
        self.type_filter = page.get_by_label("Type", exact=True)
        self.from_date = page.get_by_label("From date", exact=True)
        self.no_transactions_message = page.get_by_text(
            "No matching transactions", exact=True
        )
        
    def open(self):
        super().open("/history")

    def open_first_transaction(self):
        self.transactions.first.click()

    def filter_by_type(self, transaction_type: str):
        self.type_filter.click()
        self.page.get_by_role(
            "option", name=transaction_type, exact=True
        ).click()