import pytest

from decimal import Decimal as D

from django_pay2.providers.perfect_money.create_payment import (
    create_perfect_money_payment,
)
from django_pay2.models import Payment

pytestmark = pytest.mark.django_db


def test_create_perfect_money_payment(rf, test_invoice):
    payment_method = create_perfect_money_payment(
        rf.get("/"),
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
