from django.test import TestCase

from django_pay2.models import Payment
from django_pay2.signals import payment_received

from .models import TestInvoice
from .utils import SignalsMixin


class PaymentTests(SignalsMixin, TestCase):
    def setUp(self) -> None:
        self.invoice = TestInvoice.objects.create()
        self.payment = Payment.objects.create(amount=100, receiver=self.invoice)

    def test_accept(self):
        with self.assert_signal_sent(
            payment_received, TestInvoice, receiver=self.invoice
        ):
            self.payment.accept()
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.StatusType.SUCCESS)

    def test_reject(self):
        self.payment.reject()
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.StatusType.REJECTED)
