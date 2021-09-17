import pytest
from decimal import Decimal as D

pytestmark = pytest.mark.django_db


def test_perfect_money_api_generate_payment_method(api, rf, sample_uid):
    request = rf.get("/")

    method = api.generate_payment_method(request, D("100.00"), "USD", sample_uid)

    assert method.fields["PAYEE_ACCOUNT"] == "U123456"
    assert method.fields["PAYEE_NAME"] == "john.due"
    assert method.fields["PAYMENT_AMOUNT"] == "100.00"
    assert method.fields["PAYMENT_UNITS"] == "USD"
    assert method.fields["PAYMENT_ID"] == sample_uid
    assert "/perfect-money/notify/" in method.fields["STATUS_URL"]
    assert "/success/" in method.fields["PAYMENT_URL"]
    assert "/failed/" in method.fields["NOPAYMENT_URL"]
    assert method.fields["BAGGAGE_FIELDS"] == ""


def test_perfect_money_api_calculate_sign(api):
    sign = api.calculate_sign(
        "AB-123", D("300.00"), "USD", "789012", "U456789", "876543210"
    )

    assert sign == "1CC09524986EDC51F7BEA9E6973F5187"
