from uuid import uuid4

import pytest


@pytest.mark.regression
def test_api_bank_01_cannot_delete_another_users_account(
    api_user_a, api_user_b
):
    bank_name = f"Test Bank {uuid4().hex[:8]}"

    # יצירת חשבון זמני בבעלות B
    response = api_user_b.post(
        "/functions/v1/add-bank-account",
        data={
            "accountHolderName": "Test User",
            "bankName": bank_name,
            "country": "US",
            "currency": "USD",
            "accountIdentifier": "123456789",
        },
    )
    assert response.status == 201

    account_id = response.json()["account"]["id"]
    account_filter = {"id": f"eq.{account_id}"}

    try:
        # וידוא שהחשבון קיים ונגיש ל־B
        response = api_user_b.get(
            "/rest/v1/bank_accounts",
            params=account_filter,
        )
        assert response.status == 200

        accounts_before = response.json()
        assert len(accounts_before) == 1
        assert accounts_before[0]["bank_name"] == bank_name

        # ניסיון למחוק את החשבון באמצעות A
        delete_response = api_user_a.delete(
            "/rest/v1/bank_accounts",
            params=account_filter,
        )

        # B בודק שהחשבון שלו נשאר ללא שינוי
        response = api_user_b.get(
            "/rest/v1/bank_accounts",
            params=account_filter,
        )
        assert response.status == 200
        assert response.json() == accounts_before, (
            "User A deleted or changed user B's bank account"
        )

        assert delete_response.status in (200, 204, 401, 403), (
            f"Unexpected HTTP status: {delete_response.status}"
        )

    finally:
        # ניקוי באמצעות בעל החשבון
        response = api_user_b.delete(
            "/rest/v1/bank_accounts",
            params=account_filter,
        )
        assert response.status in (200, 204)

        response = api_user_b.get(
            "/rest/v1/bank_accounts",
            params=account_filter,
        )
        assert response.status == 200
        assert response.json() == []