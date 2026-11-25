from playwright.sync_api import Page
from pages.base_page import BasePage


class BankAccountsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_account_button = page.get_by_role(
            "button", name="Add bank account", exact=True
        )

        self.account_dialog = page.get_by_role("dialog")

        self.account_holder = self.account_dialog.get_by_label(
            "Account holder name", exact=True
        )
        self.bank_name = self.account_dialog.get_by_label(
            "Bank name", exact=True
        )
        self.account_number = self.account_dialog.get_by_label(
            "IBAN or account number", exact=True
        )

        self.save_account_button = self.account_dialog.get_by_role(
            "button", name="Add bank account", exact=True
        )

        self.country = self.account_dialog.get_by_role(
        "combobox", name="Country", exact=True
        )
        self.currency = self.account_dialog.get_by_role(
        "combobox", name="Currency", exact=True
        )

    def open(self):
        super().open("/bank-accounts")

    def open_add_account_form(self):
        self.add_account_button.click()

    def select_country(self, country: str):
        self.country.click()
        self.page.get_by_role(
        "option", name=country, exact=True
        ).click()
    
    def select_currency(self, currency: str):
        self.currency.click()
        self.page.get_by_role(
        "option", name=currency, exact=True
        ).click()

    def fill_account_details(
        self,
        holder_name: str,
        bank_name: str,
        country: str,
        currency: str,
        account_number: str,
        ):
        self.account_holder.fill(holder_name)
        self.bank_name.fill(bank_name)
        self.select_country(country)
        self.select_currency(currency)
        self.account_number.fill(account_number)
    
    def submit_account(self):
        self.save_account_button.click()

    def get_account(self, bank_name: str):
        return self.page.get_by_test_id("bank-account-item").filter(
        has_text=bank_name
        )

    def open_remove_account_dialog(self, bank_name: str):
        self.get_account(bank_name).get_by_role(
        "button", name=f"Remove {bank_name} account"
        ).click()

    def confirm_account_removal(self):
        self.page.get_by_role(
        "button", name="Remove", exact=True
        ).click()

    def remove_account(self, bank_name: str):
        self.open_remove_account_dialog(bank_name)
        self.confirm_account_removal()