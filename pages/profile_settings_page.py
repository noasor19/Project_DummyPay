from playwright.sync_api import Page

from pages.base_page import BasePage


class ProfileSettingsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = page.get_by_role(
            "heading", name="Profile & Settings", exact=True
        )
        self.display_name = page.get_by_label(
            "Display name", exact=True
        )
        self.save_button = page.get_by_role(
            "button", name="Save", exact=True
        )
        self.saved_display_name = page.locator("dl > div").filter(
        has=page.locator("dt").filter(has_text="Display name")
        ).locator("dd")
        self.user_menu_button = page.locator(
        'aside button[data-slot="dropdown-menu-trigger"]'
        )
        self.sign_out_item = page.get_by_role(
        "menuitem", name="Sign out", exact=True
        )

    def open(self):
        super().open("/settings")

    def update_display_name(self, name: str):
        self.display_name.fill(name)
        self.save_button.click()

    def sign_out(self):
        self.user_menu_button.click()
        self.sign_out_item.click()