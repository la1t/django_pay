import pytest
from django.urls import reverse
from rest_framework import status

from django_pay2.models import Payment

pytestmark = pytest.mark.django_db


def test_qiwi_notify_view(settings, sample_uid, payment_factory, client):
    settings.PAYMENTS = {"QIWI": {"secret_key": "qwerty"}}
    url = reverse("django_pay2:qiwi:notify")
    payment = payment_factory(id=sample_uid, amount=10)

    response = client.post(
        url,
        {
            "bill": {
                "siteId": "1234",
                "billId": sample_uid,
                "amount": {"value": "10.00", "currency": "RUB"},
                "status": {
                    "value": "PAID",
                },
            }
        },
        HTTP_X_API_SIGNATURE_SHA256="4dce0933f565dde1b45bc73ccb91af755fcad313751371de9688521e5b49b9f4",
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
    payment.refresh_from_db()
    assert payment.status == Payment.StatusType.SUCCESS
