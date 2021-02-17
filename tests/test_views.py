from http import HTTPStatus
from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from django_pay2.models import Payment

from .models import TestInvoice


class BasePaymentTestCase(TestCase):
    def setUp(self) -> None:
        self.invoice = TestInvoice.objects.create()
        self.pending_payment = Payment.objects.create(amount=100, receiver=self.invoice)
        self.success_payment = Payment.objects.create(
            amount=100, receiver=self.invoice, status=Payment.StatusType.SUCCESS
        )


class DebugViewsTests(BasePaymentTestCase):
    def test_debug_payment_does_not_available_with_debug_off(self):
        url = reverse("django_pay2:debug_payment", args=[self.pending_payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_debug_accept_does_not_available_with_debug_off(self):
        url = reverse("django_pay2:debug_accept", args=[self.pending_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_debug_reject_dont_available_with_debug_off(self):
        url = reverse("django_pay2:debug_reject", args=[self.pending_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


@override_settings(PAYMENTS={"DEBUG_MODE": True})
class DebugPaymentTests(BasePaymentTestCase):
    def test_render(self):
        url = reverse("django_pay2:debug_payment", args=[self.pending_payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_work_only_with_pending_payments(self):
        url = reverse("django_pay2:debug_payment", args=[self.success_payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


@override_settings(PAYMENTS={"DEBUG_MODE": True})
class AcceptDebugPaymentTests(BasePaymentTestCase):
    @mock.patch("django_pay2.models.Payment.accept")
    def test_accept_payment(self, mocked_accept):
        url = reverse("django_pay2:debug_accept", args=[self.pending_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("django_pay2:success"))
        mocked_accept.assert_called_once()

    def test_work_only_with_pending_payments(self):
        url = reverse("django_pay2:debug_accept", args=[self.success_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


@override_settings(PAYMENTS={"DEBUG_MODE": True})
class RejectDebugPaymentTests(BasePaymentTestCase):
    @mock.patch("django_pay2.models.Payment.reject")
    def test_reject_payment(self, mocked_reject):
        url = reverse("django_pay2:debug_reject", args=[self.pending_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, reverse("django_pay2:fail"))
        mocked_reject.assert_called_once()

    def test_work_only_with_pending_payments(self):
        url = reverse("django_pay2:debug_reject", args=[self.success_payment.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class SuccessPaymentTests(TestCase):
    def test_render_default_template(self):
        url = reverse("django_pay2:success")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "django_pay2/success_payment.html")

    @override_settings(PAYMENTS={"TEMPLATES": {"success": "test.html"}})
    def test_override_template(self):
        url = reverse("django_pay2:success")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "test.html")


class RejectedPaymentTests(TestCase):
    def test_render_default_template(self):
        url = reverse("django_pay2:fail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            "django_pay2/rejected_payment.html",
        )

    @override_settings(PAYMENTS={"TEMPLATES": {"rejected": "test.html"}})
    def test_override_template(self):
        url = reverse("django_pay2:fail")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "test.html")
