from playwright.sync_api import Page

from pages.base_page import BasePage


class PaymentCardsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_card_button = page.get_by_role(
            "button", name="Add card", exact=True
        )

        self.card_dialog = page.get_by_role("dialog")
        self.cardholder_name = self.card_dialog.get_by_label(
            "Cardholder name", exact=True
        )
        self.card_number = self.card_dialog.get_by_label(
            "Card number", exact=True
        )
        self.expiry = self.card_dialog.get_by_label(
            "Expiry (MM/YY)", exact=True
        )
        self.cvv = self.card_dialog.get_by_label("CVV", exact=True)
        self.save_card_button = self.card_dialog.get_by_role(
            "button", name="Add card", exact=True
        )

    def open(self):
        super().open("/cards")

    def open_add_card_form(self):
        self.add_card_button.click()

    def fill_card_details(
        self,
        name: str,
        number: str,
        expiry: str,
        cvv: str,
    ):
        self.cardholder_name.fill(name)
        self.card_number.fill(number)
        self.expiry.fill(expiry)
        self.cvv.fill(cvv)

    def submit_card(self):
        self.save_card_button.click()

    def confirm_card_removal(self):
        self.page.get_by_role(
            "button", name="Remove", exact=True
        ).click()

    def get_card(self, name: str):
        return self.page.get_by_test_id("card-item").filter(
            has_text=name
        )

    def remove_card(self, name: str):
        card = self.get_card(name)
        card.get_by_role(
            "button", name="Remove card ending in"
        ).click()
        self.confirm_card_removal()