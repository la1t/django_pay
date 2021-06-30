from django.urls import reverse
import pytest
from rest_framework import status
from django_pay2.models import Payment
from urllib.parse import urlencode

pytestmark = pytest.mark.django_db


class TestCoinPaymentsNotify:
    @pytest.fixture
    def url(self):
        return reverse("django_pay2:coinpayments:notify")

    def test_positive(self, mocker, api, sample_uid, payment_factory, client, url):
        payment = payment_factory(id=sample_uid)
        mocker.patch(
            "django_pay2.providers.coinpayments.views.get_api", return_value=api
        )
        data = {
            "status": 100,
            "invoice": sample_uid,
        }

        response = client.post(
            url,
            urlencode(data),
            HTTP_HMAC=(
                "ffdcba12729150a031059f4d28487ada1a55ba3f93a"
                "535cfd0dc1d6645844d3e6ca14256b8c763ca338ec70f6474cabef3c0b13606e8f4e940ee0ce7a94992aa"
            ),
            content_type="application/x-www-form-urlencoded",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content == b"IPN OK"
        payment.refresh_from_db()
        assert payment.status == Payment.StatusType.SUCCESS

    def test_if_incorrect_hmac(
        self, mocker, api, sample_uid, payment_factory, client, url
    ):
        payment_factory(id=sample_uid)
        mocker.patch(
            "django_pay2.providers.coinpayments.views.get_api", return_value=api
        )
        data = {
            "status": 100,
            "invoice": sample_uid,
        }

        response = client.post(
            url,
            urlencode(data),
            HTTP_HMAC="incorrect",
            content_type="application/x-www-form-urlencoded",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content.decode("utf-8").startswith("IPN Error")

    def test_if_validation_error(self, mocker, api, sample_uid, client, url):
        mocker.patch(
            "django_pay2.providers.coinpayments.views.get_api", return_value=api
        )
        data = {
            "status": 100,
            "invoice": sample_uid,
        }

        response = client.post(
            url,
            urlencode(data),
            HTTP_HMAC=(
                "ffdcba12729150a031059f4d28487ada1a55ba3f93a"
                "535cfd0dc1d6645844d3e6ca14256b8c763ca338ec70f6474cabef3c0b13606e8f4e940ee0ce7a94992aa"
            ),
            content_type="application/x-www-form-urlencoded",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content.decode("utf-8").startswith("IPN Error")
