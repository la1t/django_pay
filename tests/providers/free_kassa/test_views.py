import pytest
from django.urls import reverse
from rest_framework import status

from django_pay2.models import Payment

pytestmark = pytest.mark.django_db


class TestNotifyView:
    @pytest.fixture
    def url(self):
        return reverse("django_pay2:free_kassa:notify")

    def test_positive(self, payment_factory, sample_uid, client, url):
        payment = payment_factory(id=sample_uid, amount=100)

        response = client.post(
            url,
            {
                "MERCHANT_ID": "qwerty",
                "AMOUNT": 100.0,
                "MERCHANT_ORDER_ID": sample_uid,
                "SIGN": "aee8dcfb58b752160ed9e650a0d6b59f",
            },
            format="multipart",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content == b"YES"
        payment.refresh_from_db()
        assert payment.status == Payment.StatusType.SUCCESS

    def test_error(self, payment_factory, sample_uid, client, url):
        payment_factory(id=sample_uid, amount=100)

        response = client.post(
            url,
            {
                "MERCHANT_ID": "qwerty",
                "AMOUNT": 100,
                "MERCHANT_ORDER_ID": sample_uid,
                "SIGN": "incorrect",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content == b"NO: Incorrect sign"
