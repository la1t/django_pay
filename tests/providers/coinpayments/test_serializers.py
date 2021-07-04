import pytest

from django_pay2.providers.coinpayments.serializers import CoinPaymentsApproveSerializer

pytestmark = pytest.mark.django_db


class TestCoinPaymentsApproveSerializer:
    def test_if_not_done_status(self, payment):
        serializer = CoinPaymentsApproveSerializer(
            data={
                "invoice": payment.pk,
                "status": 10,
            }
        )

        assert not serializer.is_valid()

    def test_positive(self, payment):
        serializer = CoinPaymentsApproveSerializer(
            data={
                "invoice": payment.id,
                "status": 100,
            }
        )

        assert serializer.is_valid()
