import pytest

from utilities.config import SUPABASE_URL, SUPABASE_ANON_KEY, USER_A_EMAIL, USER_A_PASSWORD


@pytest.fixture
def anonymous_request(playwright):
    # A request with the project key only, no user token (not logged in)
    request = playwright.request.new_context(
        base_url=SUPABASE_URL,
        extra_http_headers={"apikey": SUPABASE_ANON_KEY},
    )
    yield request
    request.dispose()


def login(request, email: str, password: str):
    return request.post(
        "/auth/v1/token?grant_type=password",
        data={"email": email, "password": password},
    )


@pytest.mark.regression
def test_api_auth_01_login_valid(anonymous_request):
    """TC-API-AUTH-01: Valid login returns HTTP 200 and an access token"""
    response = login(anonymous_request, USER_A_EMAIL, USER_A_PASSWORD)
    assert response.status == 200
    assert response.json()["access_token"]


@pytest.mark.regression
def test_api_auth_02_login_wrong_password(anonymous_request):
    """TC-API-AUTH-02: Wrong password returns HTTP 400 and an error message"""
    response = login(anonymous_request, USER_A_EMAIL, "wrong123")
    assert response.status == 400
    assert response.json()["msg"] == "Invalid login credentials"


@pytest.mark.regression
def test_api_wallet_02_get_wallets(api_user_a):
    """TC-API-WALLET-02: A logged-in user can read their wallets"""
    response = api_user_a.get("/rest/v1/wallets", params={"select": "currency,balance_minor"})
    assert response.status == 200
    currencies = [wallet["currency"] for wallet in response.json()]
    assert "ILS" in currencies


@pytest.mark.regression
def test_api_wallet_03_get_wallets_without_login(anonymous_request):
    """TC-API-WALLET-03: Reading wallets without a token is rejected with HTTP 401"""
    response = anonymous_request.get("/rest/v1/wallets", params={"select": "currency,balance_minor"})
    assert response.status == 401