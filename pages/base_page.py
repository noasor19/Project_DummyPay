from playwright.sync_api import Page

from utilities.config import BASE_URL


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str):
        self.page.goto(f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}")