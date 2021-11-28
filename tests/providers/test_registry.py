import pytest

from django_pay2.providers.registry import get_payment_system_choices


@pytest.fixture(autouse=True)
def set_enbaled_payment_systems(settings):
    settings.PAYMENTS = {"ENABLED_PAYMENT_SYSTEMS": ["tinkoff", "sberbank"]}


def test_get_payment_system_choices():
    assert get_payment_system_choices() == [
        ("tinkoff", "Тинькофф"),
        ("sberbank", "Сбербанк"),
    ]
