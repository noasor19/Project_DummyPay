from uuid import uuid4

import pytest
from playwright.sync_api import expect

from pages.profile_settings_page import ProfileSettingsPage
import re
from utilities.test_data import INVALID_DISPLAY_NAME_MESSAGE

@pytest.mark.regression
def test_prof_01_update_display_name(logged_in_page_b):
    profile_page = ProfileSettingsPage(logged_in_page_b)
    profile_page.open()

    expect(profile_page.saved_display_name).to_be_visible()
    original_name = profile_page.saved_display_name.inner_text()
    new_name = f"Test User {uuid4().hex[:8]}"

    try:
        profile_page.update_display_name(new_name)

        expect(profile_page.saved_display_name).to_have_text(new_name)

        logged_in_page_b.reload()

        expect(profile_page.saved_display_name).to_have_text(new_name)
        expect(profile_page.display_name).to_have_value(new_name)

    finally:
        profile_page.update_display_name(original_name)
        expect(profile_page.saved_display_name).to_have_text(
            original_name
        )

@pytest.mark.smoke
@pytest.mark.regression
def test_prof_03_sign_out(logged_in_page_b):
    profile_page = ProfileSettingsPage(logged_in_page_b)
    profile_page.open()
    expect(profile_page.heading).to_be_visible()

    profile_page.sign_out()

    expect(logged_in_page_b).to_have_url(
        re.compile(r"/login(?:\?.*)?$")
    )
    expect(
        logged_in_page_b.get_by_role(
            "button", name="Sign in", exact=True
        )
    ).to_be_visible()

    profile_page.open()

    expect(logged_in_page_b).to_have_url(
        re.compile(r"/login(?:\?.*)?$")
    )

@pytest.mark.regression
def test_prof_04_empty_display_name(logged_in_page_b):
    profile_page = ProfileSettingsPage(logged_in_page_b)
    profile_page.open()

    expect(profile_page.saved_display_name).to_be_visible()
    original_name = profile_page.saved_display_name.inner_text()

    profile_page.update_display_name("")

    expect(
        logged_in_page_b.get_by_text(
            INVALID_DISPLAY_NAME_MESSAGE, exact=True
        )
    ).to_be_visible()

    expect(profile_page.saved_display_name).to_have_text(original_name)

    logged_in_page_b.reload()

    expect(profile_page.saved_display_name).to_have_text(original_name)
    expect(profile_page.display_name).to_have_value(original_name)

@pytest.mark.regression
def test_prof_05_single_character_display_name(logged_in_page_b):
    profile_page = ProfileSettingsPage(logged_in_page_b)
    profile_page.open()

    expect(profile_page.saved_display_name).to_be_visible()
    original_name = profile_page.saved_display_name.inner_text()

    profile_page.update_display_name("A")

    expect(
        logged_in_page_b.get_by_text(
            INVALID_DISPLAY_NAME_MESSAGE, exact=True
        )
    ).to_be_visible()

    expect(profile_page.saved_display_name).to_have_text(original_name)

    logged_in_page_b.reload()

    expect(profile_page.saved_display_name).to_have_text(original_name)
    expect(profile_page.display_name).to_have_value(original_name)

@pytest.mark.regression
def test_prof_06_spaces_only_display_name(logged_in_page_b):
    profile_page = ProfileSettingsPage(logged_in_page_b)
    profile_page.open()

    expect(profile_page.saved_display_name).to_be_visible()
    original_name = profile_page.saved_display_name.inner_text()

    profile_page.update_display_name("   ")

    expect(
        logged_in_page_b.get_by_text(
            INVALID_DISPLAY_NAME_MESSAGE, exact=True
        )
    ).to_be_visible()

    expect(profile_page.saved_display_name).to_have_text(original_name)

    logged_in_page_b.reload()

    expect(profile_page.saved_display_name).to_have_text(original_name)
    expect(profile_page.display_name).to_have_value(original_name)