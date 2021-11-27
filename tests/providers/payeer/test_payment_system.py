import pytest

from decimal import Decimal

from django_pay2.providers.payeer.payment_system import Payeer
from django_pay2.providers.payeer.api import PayeerError
from django_pay2.models import Payment
from django_pay2.exceptions import CreatePaymentError

pytestmark = pytest.mark.django_db


def test_positive(mocker, rf, test_invoice):
    mocker.patch(
        "django_pay2.providers.payeer.api.PayeerApi.create_payment",
        return_value="https://example.com",
    )
    payment_url = Payeer().create_payment(
        receiver=test_invoice,
        amount=Decimal(100),
        currency="USD",
        desc="Test",
    )

    assert payment_url == "https://example.com"
    assert Payment.objects.count() == 1
    payment = Payment.objects.get()
    assert payment.amount == Decimal(100)
    assert payment.receiver == test_invoice
    assert payment.status == Payment.StatusType.PENDING


def test_reject_payment_and_raise_err_if_payeer_api_returned_err(
    mocker, rf, test_invoice
):
    mocker.patch(
        "django_pay2.providers.payeer.api.PayeerApi.create_payment",
        side_effect=PayeerError(["test"]),
    )

    with pytest.raises(CreatePaymentError):
        Payeer().create_payment(
            request=rf.get("/"),
            receiver=test_invoice,
            amount=Decimal(100),
            currency="USD",
            desc="Test",
        )
