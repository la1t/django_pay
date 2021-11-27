from decimal import Decimal as D

import pytest

from django_pay2.models import Payment
from django_pay2.providers.perfect_money.payment_system import PerfectMoney

pytestmark = pytest.mark.django_db


def test_create_perfect_money_payment(rf, test_invoice):
    payment_method = PerfectMoney().create_payment(
        request=rf.get("/"),
        receiver=test_invoice,
        amount=D("100.00"),
        currency="USD",
        desc="Test",
    )

    assert payment_method.method == "form"
    assert Payment.objects.count() == 1
    payment = Payment.objects.get()
    assert payment.amount == D("100")
    assert payment.receiver == test_invoice
    assert payment.status == Payment.StatusType.PENDING
