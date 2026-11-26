from uuid import uuid4

import pytest

from utilities.config import USER_B_EMAIL


def get_balance(api, currency):
    response = api.get(
        "/rest/v1/wallets",
        params={
            "currency": f"eq.{currency}",
            "select": "balance_minor",
        },
    )
    assert response.status == 200

    wallets = response.json()
    return wallets[0]["balance_minor"] if wallets else 0


@pytest.mark.regression
def test_api_send_01_updates_both_balances(api_user_a, api_user_b):
    # איתור משתמש B
    response = api_user_a.post(
        "/rest/v1/rpc/lookup_recipient",
        data={"p_email": USER_B_EMAIL},
    )
    assert response.status == 200

    recipients = response.json()
    assert len(recipients) == 1

    recipient = recipients[0]
    assert recipient["status"] == "found"

    sending_currency = "ILS"
    receiving_currency = recipient["preferred_currency"]
    amount_minor = 100  # 100 אגורות = שקל אחד

    sender_before = get_balance(api_user_a, sending_currency)
    recipient_before = get_balance(api_user_b, receiving_currency)
    assert sender_before >= amount_minor, "Insufficient test balance"

    # יצירת הצעת העברה, כולל שער ההמרה
    response = api_user_a.post(
        "/rest/v1/rpc/create_transfer_quote",
        data={
            "p_recipient_id": recipient["user_id"],
            "p_sending_currency": sending_currency,
            "p_amount_minor": amount_minor,
            "p_input_side": "send",
        },
    )
    assert response.status == 200

    quote = response.json()
    assert quote["sending_amount_minor"] == amount_minor
    assert quote["receiving_currency"] == receiving_currency
    assert quote["receiving_amount_minor"] > 0

    # ביצוע ההעברה
    response = api_user_a.post(
        "/rest/v1/rpc/execute_transfer",
        data={
            "p_quote_id": quote["quote_id"],
            "p_idempotency_key": str(uuid4()),
        },
    )
    assert response.status == 200

    transaction = response.json()
    assert transaction["status"] == "completed"
    assert transaction["recipient_user_id"] == recipient["user_id"]
    assert transaction["sending_amount_minor"] == amount_minor
    assert (
        transaction["receiving_amount_minor"]
        == quote["receiving_amount_minor"]
    )

    # בדיקת השינוי המדויק בשתי היתרות
    sender_after = get_balance(api_user_a, sending_currency)
    recipient_after = get_balance(api_user_b, receiving_currency)

    assert sender_after == sender_before - amount_minor
    assert (
        recipient_after
        == recipient_before + quote["receiving_amount_minor"]
    )

@pytest.mark.regression
def test_api_send_02_retry_does_not_charge_twice(
    api_user_a, api_user_b
):
    response = api_user_a.post(
        "/rest/v1/rpc/lookup_recipient",
        data={"p_email": USER_B_EMAIL},
    )
    assert response.status == 200

    recipients = response.json()
    assert len(recipients) == 1

    recipient = recipients[0]
    assert recipient["status"] == "found"

    sending_currency = "ILS"
    receiving_currency = recipient["preferred_currency"]
    amount_minor = 100

    sender_before = get_balance(api_user_a, sending_currency)
    recipient_before = get_balance(api_user_b, receiving_currency)
    assert sender_before >= amount_minor, "Insufficient test balance"

    response = api_user_a.post(
        "/rest/v1/rpc/create_transfer_quote",
        data={
            "p_recipient_id": recipient["user_id"],
            "p_sending_currency": sending_currency,
            "p_amount_minor": amount_minor,
            "p_input_side": "send",
        },
    )
    assert response.status == 200

    quote = response.json()
    assert quote["sending_amount_minor"] == amount_minor
    assert quote["receiving_currency"] == receiving_currency
    assert quote["receiving_amount_minor"] > 0

    # שתי הבקשות משתמשות באותה הצעה ובאותו מפתח
    transfer_data = {
        "p_quote_id": quote["quote_id"],
        "p_idempotency_key": str(uuid4()),
    }

    first_response = api_user_a.post(
        "/rest/v1/rpc/execute_transfer",
        data=transfer_data,
    )
    assert first_response.status == 200

    first_transaction = first_response.json()
    assert first_transaction["status"] == "completed"
    assert first_transaction["id"]

    second_response = api_user_a.post(
        "/rest/v1/rpc/execute_transfer",
        data=transfer_data,
    )
    assert second_response.status == 200

    second_transaction = second_response.json()

    assert second_transaction["id"] == first_transaction["id"]
    assert second_transaction["status"] == "completed"

    # אחרי שתי הבקשות, הכסף עבר פעם אחת בלבד
    sender_after = get_balance(api_user_a, sending_currency)
    recipient_after = get_balance(api_user_b, receiving_currency)

    assert sender_after == sender_before - amount_minor
    assert (
        recipient_after
        == recipient_before + quote["receiving_amount_minor"]
    )