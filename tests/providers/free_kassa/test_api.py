from django_pay2.providers.free_kassa.api import FreeKassaApi
import pytest
import uuid

pytestmark = pytest.mark.django_db


@pytest.fixture
def api():
    return FreeKassaApi(
        merchant_id="qwerty", secret_word_1="qwerty", secret_word_2="qwerty"
    )


@pytest.fixture
def uid():
    return uuid.UUID("9234e6e7-d737-40f8-8fd3-e876116aab0b")


def test_generate_form(api, uid):
    payment_method = api.generate_payment_method(100, uid)

    assert payment_method.method == "form"
    assert payment_method.url == "https://www.free-kassa.ru/merchant/cash.php"
    assert payment_method.fields.get("m") == "qwerty"
    assert payment_method.fields.get("oa") == "100"
    assert payment_method.fields.get("o") == str(uid)
    assert payment_method.fields.get("s") == "aee8dcfb58b752160ed9e650a0d6b59f"
