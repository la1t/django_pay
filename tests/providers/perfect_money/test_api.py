import pytest
from decimal import Decimal as D

pytestmark = pytest.mark.django_db


def test_perfect_money_api_generate_payment_method(api, rf, sample_uid):
    request = rf.get("/")

    method = api.generate_payment_method(request, D("100.00"), "USD", sample_uid)

    assert method.fields["payee_account"] == "U123456"
    assert method.fields["payee_name"] == "john.due"
    assert method.fields["payment_amount"] == "100.00"
    assert method.fields["payment_units"] == "USD"
    assert method.fields["payment_id"] == sample_uid
    assert "/perfect-money/notify/" in method.fields["status_url"]
    assert "/success/" in method.fields["payment_url"]
    assert "/failed/" in method.fields["nopayment_url"]
    assert method.fields["baggage_fields"] == ""


def test_perfect_money_api_calculate_sign(api):
    sign = api.calculate_sign(
        "AB-123", D("300.00"), "USD", "789012", "U456789", "876543210"
    )

    assert sign == "1CC09524986EDC51F7BEA9E6973F5187"
