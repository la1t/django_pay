import pytest

from django_pay2.models import Payment
from django_pay2.signals import payment_received

from .models import TestInvoice
from .utils import assert_signal_sent

pytestmark = pytest.mark.django_db


@pytest.fixture
def invoice():
    return TestInvoice.objects.create()


@pytest.fixture
def payment(invoice):
    return Payment.objects.create(amount=100, receiver=invoice)


def test_payment_accept(invoice, payment):
    with assert_signal_sent(payment_received, TestInvoice, receiver=invoice):
        payment.accept()

    payment.refresh_from_db()
    assert payment.status == Payment.StatusType.SUCCESS


def test_payment_reject(payment):
    payment.reject()

    payment.refresh_from_db()
    assert payment.status == Payment.StatusType.REJECTED
