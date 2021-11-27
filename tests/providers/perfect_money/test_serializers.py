from decimal import Decimal as D

import pytest

from django_pay2.providers.perfect_money.serializers import PerfectMoneyNotifySerializer

pytestmark = pytest.mark.django_db


class TestPerfectMoneyNotifySerializerValidate:
    def test_positive(self, mocker, api, payment_factory, sample_uid):
        payment_factory(id=sample_uid)
        mocker.patch(
            "django_pay2.providers.perfect_money.serializers.get_api", return_value=api
        )
        data = {
            "PAYEE_ACCOUNT": "U123456",
            "PAYMENT_ID": sample_uid,
            "PAYMENT_AMOUNT": D("1000.00"),
            "PAYMENT_UNITS": "USD",
            "PAYMENT_BATCH_NUM": "789012",
            "PAYER_ACCOUNT": "U456789",
            "TIMESTAMPGMT": 876543210,
            "V2_HASH": "BE45EF688D2AFC8079580D314F87D715",
        }

        serializer = PerfectMoneyNotifySerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_if_amounts_are_not_equal(self, payment_factory, sample_uid):
        payment_factory(id=sample_uid)
        data = {
            "PAYEE_ACCOUNT": "U123456",
            "PAYMENT_ID": sample_uid,
            "PAYMENT_AMOUNT": D("300.00"),
            "PAYMENT_UNITS": "USD",
            "PAYMENT_BATCH_NUM": "789012",
            "PAYER_ACCOUNT": "U456789",
            "TIMESTAMPGMT": 876543210,
            "V2_HASH": "BA23081E6828BA02A5D163E545FB9E8F",
        }

        serializer = PerfectMoneyNotifySerializer(data=data)

        assert not serializer.is_valid()
