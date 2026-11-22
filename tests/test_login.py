import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.regression
def test_login_user_a(logged_in_page_a):
    expect(
        logged_in_page_a.get_by_role(
            "heading", name="Dashboard", exact=True
        )
    ).to_be_visible()


@pytest.mark.smoke
@pytest.mark.regression
def test_login_user_b(logged_in_page_b):
    expect(
        logged_in_page_b.get_by_role(
            "heading", name="Dashboard", exact=True
        )
    ).to_be_visible()