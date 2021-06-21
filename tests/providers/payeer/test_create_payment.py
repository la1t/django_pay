from decimal import Decimal
from django.test import TestCase
from unittest.mock import patch

from django.test.client import RequestFactory

from django_pay2.providers.payeer.create_payment import create_payeer_payment
from django_pay2.providers.payeer.api import PayeerError
from django_pay2.models import Payment
from django_pay2.exceptions import CreatePaymentError

from tests.models import TestInvoice


class TestCreatePayeerPayment(TestCase):
    req_factory = RequestFactory()

    def setUp(self) -> None:
        super().setUp()
        self.invoice = TestInvoice.objects.create()

    @patch(
        "django_pay2.providers.payeer.api.PayeerApi.create_payment",
        return_value="https://example.com",
    )
    def test_create_payment_if_payeer_api_does_not_return_errors(
        self, patched_create_payment
    ):
        payment_url = create_payeer_payment(
            self.req_factory.get("/"),
            receiver=self.invoice,
            amount=Decimal(100),
            currency="USD",
            desc="Test",
        )

        self.assertEqual(payment_url, "https://example.com")
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.get()
        self.assertEqual(payment.amount, Decimal(100))
        self.assertEqual(payment.receiver, self.invoice)
        self.assertEqual(payment.status, Payment.StatusType.PENDING)

    @patch(
        "django_pay2.providers.payeer.api.PayeerApi.create_payment",
        side_effect=PayeerError(["test"]),
    )
    def test_reject_payment_and_raise_err_if_payeer_api_returns_error(
        self, patched_created_payment
    ):
        with self.assertRaises(CreatePaymentError):
            create_payeer_payment(
                request=self.req_factory.get("/"),
                receiver=self.invoice,
                amount=Decimal(100),
                currency="USD",
                desc="Test",
            )

        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.get()
        self.assertEqual(payment.status, Payment.StatusType.REJECTED)
