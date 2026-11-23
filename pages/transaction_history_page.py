from playwright.sync_api import Page

from pages.base_page import BasePage


class TransactionHistoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role(
            "heading", name="Transaction History", exact=True
        )

    def open(self):
        super().open("/history")