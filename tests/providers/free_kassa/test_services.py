from rest_framework.exceptions import ValidationError
from django_pay2.providers.free_kassa.services import handle_notify
import pytest
from django_pay2.models import Payment
from django_pay2.settings import payment_settings, reload_app_settings

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_uid():
    return "9234e6e7-d737-40f8-8fd3-e876116aab0b"


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
                "SIGN": "14f62ce3d1aab19979913ee3855acdd1",
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
                    "SIGN": "14f62ce3d1aab19979913ee3855acdd1",
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
                    "SIGN": "14f62ce3d1aab19979913ee3855acdd1",
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
