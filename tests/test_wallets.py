import pytest
from playwright.sync_api import expect

from pages.wallets_page import WalletsPage


@pytest.mark.smoke
@pytest.mark.regression
def test_wal_01_total_balance(logged_in_page_a):
    """TC-WAL-01: Total balance equals the sum of the wallets (ILS + USD $0)"""
    wallets = WalletsPage(logged_in_page_a)
    wallets.open()
    ils_balance = wallets.ils_balance.inner_text()
    expect(wallets.total_balance).to_have_text(f"≈ {ils_balance}")


@pytest.mark.regression
def test_wal_03_conversion_preview(logged_in_page_a):
    """TC-WAL-03: Converted amount equals Amount x Rate"""
    wallets = WalletsPage(logged_in_page_a)
    wallets.open()
    wallets.amount.fill("100")
    expected = 100 * wallets.get_rate()
    expect(wallets.converted_amount).to_have_text(f"${expected:,.2f}")


@pytest.mark.regression
def test_wal_04_existing_currency_not_offered(logged_in_page_a):
    """TC-WAL-04: Currencies that already have a wallet are not in the Add wallet list"""
    wallets = WalletsPage(logged_in_page_a)
    wallets.open()
    wallets.open_currency_list()
    expect(wallets.currency_options.first).to_be_visible()
    expect(wallets.currency_options.filter(has_text="ILS")).to_have_count(0)
    expect(wallets.currency_options.filter(has_text="USD")).to_have_count(0)


@pytest.mark.regression
def test_wal_05_negative_amount(logged_in_page_a):
    """TC-WAL-05: Negative amount shows an error"""
    wallets = WalletsPage(logged_in_page_a)
    wallets.open()
    wallets.amount.fill("-100")
    expect(wallets.amount_error).to_be_visible()


@pytest.mark.regression
def test_wal_06_letters_in_amount(logged_in_page_a):
    """TC-WAL-06: Letters in the amount show an error"""
    wallets = WalletsPage(logged_in_page_a)
    wallets.open()
    wallets.amount.fill("abc")
    expect(wallets.amount_error).to_be_visible()