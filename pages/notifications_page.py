from playwright.sync_api import Page

from pages.base_page import BasePage


class NotificationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.heading = page.get_by_role(
            "heading", name="Notifications", exact=True
        )
        
        self.mark_all_read_button = page.get_by_role(
            "button", name="Mark all as read", exact=True
        )
        self.notifications = page.get_by_test_id("notification-item")

    def open(self):
        super().open("/notifications")

    def get_notification_dates(self):
        return self.notifications.locator(
        "span.text-xs"
        ).all_text_contents()