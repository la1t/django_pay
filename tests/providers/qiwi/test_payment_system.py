from django_pay2.models import Payment
from django_pay2.providers.qiwi.payment_system import Qiwi
import pytest
from decimal import Decimal as D

from django_pay2.payment_methods import PaymentRedirect

pytestmark = pytest.mark.django_db


def test_create_qiwi_payment(mocker, test_invoice, rf):
    mocker.patch(
        "django_pay2.providers.qiwi.api.QiwiApi.generate_payment_method",
        return_value=PaymentRedirect("https://example.com"),
    )

    payment_method = Qiwi().create_payment(
        amount=D("10.00"), receiver=test_invoice, currency="RUB"
    )

    assert Payment.objects.count() == 1
    payment = Payment.objects.get()
    assert payment.amount == D("10.00")
    assert payment.receiver == test_invoice
    assert payment_method.url == "https://example.com"
