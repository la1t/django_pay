import pytest

from django_pay2.providers.qiwi.serializers import QiwiNotifySerializer

pytestmark = pytest.mark.django_db


class TestQiwiNotifySerializer:
    @pytest.fixture
    def payment(self, payment_factory, sample_uid):
        return payment_factory(amount="10.00", id=sample_uid)

    @pytest.fixture(autouse=True)
    def set_qiwi_secret_key(self, settings):
        settings.PAYMENTS = {"QIWI": {"secret_key": "qwerty"}}

    def test_positive(self, sample_uid, payment):
        serializer = QiwiNotifySerializer(
            data={
                "bill": {
                    "siteId": "1234",
                    "billId": sample_uid,
                    "amount": {"value": "10.00", "currency": "RUB"},
                    "status": {
                        "value": "PAID",
                    },
                }
            },
            context={
                "hmac": "4dce0933f565dde1b45bc73ccb91af755fcad313751371de9688521e5b49b9f4"
            },
        )

        assert serializer.is_valid(), serializer.errors

    def test_if_hmac_is_invalid(self, sample_uid, payment):
        serializer = QiwiNotifySerializer(
            data={
                "bill": {
                    "siteId": "1234",
                    "billId": sample_uid,
                    "amount": {"value": "10.00", "currency": "RUB"},
                    "status": {
                        "value": "PAID",
                    },
                }
            },
            context={
                "hmac": "aef5c05b1ee219d8ff954db86020de22867304f274d894b0b725d50d9ea138b5"
            },
        )

        assert not serializer.is_valid()

    def test_if_amount_mismatches(self, sample_uid, payment):
        serializer = QiwiNotifySerializer(
            data={
                "bill": {
                    "siteId": "1234",
                    "billId": sample_uid,
                    "amount": {"value": "20.00", "currency": "RUB"},
                    "status": {
                        "value": "PAID",
                    },
                }
            },
            context={
                "hmac": "7570b3fd44b5b9f991ab975b5ba58876fd937ae2b34b078ae391b7468a6f65eb"
            },
        )

        assert not serializer.is_valid()

    def test_if_unexpected_status(self, sample_uid, payment):
        serializer = QiwiNotifySerializer(
            data={
                "bill": {
                    "siteId": "1234",
                    "billId": sample_uid,
                    "amount": {"value": "10.00", "currency": "RUB"},
                    "status": {
                        "value": "PENDING",
                    },
                }
            },
            context={
                "hmac": "6d37eb02527ba99d9e75f2a9de338497f5e154ec0c0fee614ef10e7597dd39db"
            },
        )

        assert not serializer.is_valid()
