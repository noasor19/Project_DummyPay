import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utilities.api_client import ApiClient
from utilities.config import (
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    USER_A_EMAIL,
    USER_A_PASSWORD,
    USER_B_EMAIL,
    USER_B_PASSWORD,
)


def login_as(page: Page, email: str, password: str):
    if not email or not password:
        pytest.fail("Set the test user's email and password in .env")

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(email, password)

    expect(
        page.get_by_role("heading", name="Dashboard", exact=True)
    ).to_be_visible()

    return page


@pytest.fixture
def logged_in_page_b(page: Page):
    return login_as(page, USER_B_EMAIL, USER_B_PASSWORD)


@pytest.fixture
def logged_in_page_a(page: Page):
    return login_as(page, USER_A_EMAIL, USER_A_PASSWORD)


@pytest.fixture
def logged_in_users(new_context):
    context_a = new_context()
    context_b = new_context()

    page_a = context_a.new_page()
    page_b = context_b.new_page()

    login_as(page_a, USER_A_EMAIL, USER_A_PASSWORD)
    login_as(page_b, USER_B_EMAIL, USER_B_PASSWORD)

    return page_a, page_b


@pytest.fixture
def api_client_factory(playwright):
    contexts = []

    def create_client(email: str, password: str):
        if not all([
            SUPABASE_URL,
            SUPABASE_ANON_KEY,
            email,
            password,
        ]):
            pytest.fail("Missing API configuration or user credentials")

        auth_request = playwright.request.new_context(
            base_url=SUPABASE_URL,
            extra_http_headers={
                "apikey": SUPABASE_ANON_KEY,
            },
        )

        try:
            response = auth_request.post(
                "/auth/v1/token?grant_type=password",
                data={
                    "email": email,
                    "password": password,
                },
            )

            assert response.status == 200, (
                f"API login failed: HTTP {response.status}"
            )

            access_token = response.json()["access_token"]

        finally:
            auth_request.dispose()

        request = playwright.request.new_context(
            base_url=SUPABASE_URL,
            extra_http_headers={
                "apikey": SUPABASE_ANON_KEY,
                "Authorization": f"Bearer {access_token}",
            },
        )

        contexts.append(request)
        return ApiClient(request)

    yield create_client

    for context in contexts:
        context.dispose()


@pytest.fixture
def api_user_a(api_client_factory):
    return api_client_factory(USER_A_EMAIL, USER_A_PASSWORD)


@pytest.fixture
def api_user_b(api_client_factory):
    return api_client_factory(USER_B_EMAIL, USER_B_PASSWORD)