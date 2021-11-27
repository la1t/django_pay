import pytest
from rest_framework.exceptions import ValidationError

from django_pay2.models import Payment
from django_pay2.providers.free_kassa.services import handle_notify

pytestmark = pytest.mark.django_db


class TestHandleNotify:
    @pytest.fixture(autouse=True)
    def set_free_kassa_settings(self, settings):
        settings.PAYMENTS = {
            "FREE_KASSA": {
                "merchant_id": "qwerty",
                "secret_word_2": "qwerty",
            }
        }

    def test_positive(self, payment_factory, sample_uid):
        payment = payment_factory(id=sample_uid, amount=100)

        result = handle_notify(
            {
                "MERCHANT_ID": "qwerty",
                "AMOUNT": 100.0,
                "MERCHANT_ORDER_ID": sample_uid,
                "SIGN": "aee8dcfb58b752160ed9e650a0d6b59f",
            }
        )

        assert str(result.id) == str(payment.id)
        assert result.status == Payment.StatusType.SUCCESS

    def test_raise_err_if_incorrect_merchant_id(self, payment_factory, sample_uid):
        payment_factory(id=sample_uid, amount=100)

        with pytest.raises(ValidationError):
            handle_notify(
                {
                    "MERCHANT_ID": "incorrect",
                    "AMOUNT": 100,
                    "MERCHANT_ORDER_ID": sample_uid,
                    "SIGN": "aee8dcfb58b752160ed9e650a0d6b59f",
                }
            )

    def test_raise_err_if_amounts_not_equal(self, payment_factory, sample_uid):
        payment_factory(id=sample_uid, amount=100)

        with pytest.raises(ValidationError):
            handle_notify(
                {
                    "MERCHANT_ID": "qwerty",
                    "AMOUNT": 5,
                    "MERCHANT_ORDER_ID": sample_uid,
                    "SIGN": "aee8dcfb58b752160ed9e650a0d6b59f",
                }
            )

    def test_raise_err_if_incorrect_sign(self, payment_factory, sample_uid):
        payment_factory(id=sample_uid, amount=100)

        with pytest.raises(ValidationError):
            handle_notify(
                {
                    "MERCHANT_ID": "qwerty",
                    "AMOUNT": 100,
                    "MERCHANT_ORDER_ID": sample_uid,
                    "SIGN": "incorrect",
                }
            )
