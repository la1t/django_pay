import pytest

from django_pay2.providers.coinpayments.api import CoinPaymentsApi


@pytest.fixture
def api():
    return CoinPaymentsApi(
        public_key="123456",
        private_key="qwerty",
        ipn_secret="qwe123098",
        success_url="/success/",
        cancel_url="/cancel/",
    )
