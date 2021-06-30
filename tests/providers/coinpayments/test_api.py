from django_pay2.providers.coinpayments.api import CoinPaymentsApi
import pytest
from decimal import Decimal as D
from unittest.mock import MagicMock

pytestmark = pytest.mark.django_db


class TestGeneratePaymentMethod:
    def test_positive(self, mocker, api, rf):
        checkout_url = (
            "https://www.coinpayments.net/index.php?cmd=checkout&id=XXX&key=ZZZ"
        )
        resp = MagicMock()
        resp.json.return_value = {
            "error": "ok",
            "result": {
                "amount": "1.00000000",
                "address": "ZZZ",
                "dest_tag": "YYY",
                "txn_id": "XXX",
                "confirms_needed": "10",
                "timeout": 9000,
                "checkout_url": checkout_url,
                "status_url": "https://www.coinpayments.net/index.php?cmd=status&id=XXX&key=ZZZ",
                "qrcode_url": "https://www.coinpayments.net/qrgen.php?id=XXX&key=ZZZ",
            },
        }
        mocker.patch("requests.post", return_value=resp)
        request = rf.get("/")

        method = api.generate_payment_method(
            request, D("1.0000000"), "BTC", "111", "a@b.ru"
        )

        assert method.url == checkout_url
