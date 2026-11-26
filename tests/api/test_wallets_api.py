import pytest


@pytest.mark.regression
def test_api_wallet_01_balance_cannot_be_changed_directly(api_user_a):
    # קריאת הארנק והיתרה המקורית
    response = api_user_a.get(
        "/rest/v1/wallets",
        params={
            "currency": "eq.ILS",
            "select": "id,balance_minor",
        },
    )
    assert response.status == 200

    wallets = response.json()
    assert len(wallets) == 1, "Expected one ILS wallet"

    wallet = wallets[0]
    original_balance = wallet["balance_minor"]

    # ניסיון לשנות יתרה ישירות, ללא העברה
    response = api_user_a.patch(
        "/rest/v1/wallets",
        params={"id": f"eq.{wallet['id']}"},
        data={"balance_minor": original_balance + 100},
    )

    # קוראים מחדש גם אם בקשת העדכון הצליחה בטעות
    balance_response = api_user_a.get(
        "/rest/v1/wallets",
        params={
            "id": f"eq.{wallet['id']}",
            "select": "id,balance_minor",
        },
    )
    assert balance_response.status == 200

    wallets_after = balance_response.json()
    assert len(wallets_after) == 1, "Wallet is missing"

    assert wallets_after[0]["balance_minor"] == original_balance, (
        "Wallet balance changed through a direct PATCH request"
    )
    assert response.status in (401, 403), (
        f"Expected access rejection, received HTTP {response.status}"
    )