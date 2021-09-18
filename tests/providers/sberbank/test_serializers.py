import pytest

from django_pay2.providers.sberbank.serializers import SberbankCallbackSerializer

pytestmark = pytest.mark.django_db


class TestSberbankCallbackSerializer:
    def test_valid(self, sample_uid, payment_factory):
        payment_factory(id=sample_uid, amount=10)

        serializer = SberbankCallbackSerializer(
            data={
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "97863CAFE54929FE82B7546787BEF68591494199D4262FBBA0650380CF3AEF10",
                "operation": "approved",
                "status": 1,
            }
        )

        assert serializer.is_valid(), serializer.errors

    def test_not_valid_if_payment_does_not_exist(self, sample_uid):
        serializer = SberbankCallbackSerializer(
            data={
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "97863CAFE54929FE82B7546787BEF68591494199D4262FBBA0650380CF3AEF10",
                "operation": "approved",
                "status": 1,
            }
        )

        assert not serializer.is_valid(), serializer.errors

    def test_not_valid_if_mismatch_amount(self, sample_uid, payment_factory):
        payment_factory(id=sample_uid, amount=5)

        serializer = SberbankCallbackSerializer(
            data={
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "97863CAFE54929FE82B7546787BEF68591494199D4262FBBA0650380CF3AEF10",
                "operation": "approved",
                "status": 1,
            }
        )

        assert not serializer.is_valid()

    def test_not_valid_if_invalid_checksum(self, sample_uid, payment_factory):
        payment_factory(id=sample_uid, amount=10)

        serializer = SberbankCallbackSerializer(
            data={
                "amount": "10",
                "mdOrder": "cd2d0800-0b2b-433b-98a5-52a0292d894b",
                "orderNumber": str(sample_uid),
                "checksum": "invalid",
                "operation": "approved",
                "status": 1,
            }
        )

        assert not serializer.is_valid()
