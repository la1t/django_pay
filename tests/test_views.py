from http import HTTPStatus
import pytest

from django.urls import reverse

from django_pay2.models import Payment

from .models import TestInvoice


pytestmark = pytest.mark.django_db


@pytest.fixture
def invoice():
    return TestInvoice.objects.create()


@pytest.fixture
def pending_payment(invoice):
    return Payment.objects.create(amount=100, receiver=invoice)


@pytest.fixture
def success_payment(invoice):
    return Payment.objects.create(
        amount=100, receiver=invoice, status=Payment.StatusType.SUCCESS
    )


@pytest.mark.parametrize(
    "url_name",
    [
        "django_pay2:debug_payment",
        "django_pay2:debug_accept",
        "django_pay2:debug_reject",
    ],
)
def test_debug_view_is_not_available_with_debug_off(pending_payment, url_name, client):
    response = client.get(reverse(url_name, args=[pending_payment.id]))

    assert response.status_code == HTTPStatus.NOT_FOUND


class DebugModeEnabledMixin:
    @pytest.fixture(autouse=True)
    def enable_debug_mode(self, settings):
        settings.PAYMENTS = {"DEBUG_MODE": True}


class TestDebugPayment(DebugModeEnabledMixin):
    def test_positive(self, pending_payment, client):
        url = reverse("django_pay2:debug_payment", args=[pending_payment.id])

        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

    def test_return_404_if_not_pending_payment(self, success_payment, client):
        url = reverse("django_pay2:debug_payment", args=[success_payment.id])

        response = client.get(url)

        assert response.status_code == HTTPStatus.NOT_FOUND


class TestAcceptDebugPayment(DebugModeEnabledMixin):
    def test_positive(self, mocker, pending_payment, client):
        mocked_accept = mocker.patch("django_pay2.models.Payment.accept")

        response = client.post(
            reverse("django_pay2:debug_accept", args=[pending_payment.id])
        )

        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("django_pay2:success")
        mocked_accept.assert_called_once()

    def test_return_404_if_not_pending_payment(self, success_payment, client):
        response = client.post(
            reverse("django_pay2:debug_accept", args=[success_payment.id])
        )

        assert response.status_code == HTTPStatus.NOT_FOUND


class TestRejectDebugPayment(DebugModeEnabledMixin):
    def test_positive(self, mocker, pending_payment, client):
        mocked_reject = mocker.patch("django_pay2.models.Payment.reject")

        response = client.post(
            reverse("django_pay2:debug_reject", args=[pending_payment.id])
        )
        assert response.url == reverse("django_pay2:fail")
        mocked_reject.assert_called_once()

    def test_return_404_if_not_pending_payment(self, success_payment, client):
        response = client.post(
            reverse("django_pay2:debug_reject", args=[success_payment.id])
        )

        assert response.status_code == HTTPStatus.NOT_FOUND


class TestSuccessPayment:
    def test_render_default_template(self, client):
        response = client.get(reverse("django_pay2:success"))

        assert response.status_code == HTTPStatus.OK
