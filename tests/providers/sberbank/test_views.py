import pytest
from django.urls import reverse
from django_pay2.models import Payment

pytestmark = pytest.mark.django_db


class TestSberbankCallbackView:
    url_name = "django_pay2:sberbank:callback"

    @pytest.fixture
    def payment(self, sample_uid, payment_factory):
        return payment_factory(id=sample_uid, amount=10)

    def test_accept_payment(self, sample_uid, client, payment):
        r = client.get(
            reverse(self.url_name),
            {
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "97863CAFE54929FE82B7546787BEF68591494199D4262FBBA0650380CF3AEF10",
                "operation": "approved",
                "status": "1",
            },
        )

        assert r.status_code == 200
        payment.refresh_from_db()
        assert payment.status == Payment.StatusType.SUCCESS

    @pytest.mark.usefixtures("payment")
    def test_return_err_if_data_is_invalid(self, sample_uid, client):
        r = client.get(
            reverse(self.url_name),
            {
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "invalid",
                "operation": "approved",
                "status": 1,
            },
        )

        assert r.status_code == 400

    def test_not_accept_payment_if_operation_is_not_approved(
        self, sample_uid, client, payment
    ):
        r = client.get(
            reverse(self.url_name),
            {
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "02A60BC14F06D7C932BF70CDC225906EFE2AEE9A12BD293504EA7768FFF4F340",
                "operation": "declinedByTimeout",
                "status": "1",
            },
        )

        assert r.status_code == 200
        payment.refresh_from_db()
        assert payment.status != Payment.StatusType.SUCCESS

    def test_not_accept_payment_if_status_is_not_success(
        self, sample_uid, client, payment
    ):
        r = client.get(
            reverse(self.url_name),
            {
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "14F4305EA16AA8889892EFB4D4068080A8BE26462088CAD2AEC1A2AACF90CB2D",
                "operation": "approved",
                "status": "0",
            },
        )

        assert r.status_code == 200
        payment.refresh_from_db()
        assert payment.status != Payment.StatusType.SUCCESS
