from django_pay2.providers.tinkoff.api.api import TinkoffApi, TinkoffOrderItem
import pytest

import responses


@responses.activate
class TestInitPayment:
    @pytest.fixture
    def api(self):
        return TinkoffApi("terminal_key", "password")

    @pytest.fixture
    def valid_response(self):
        return {
            "Success": True,
            "PaymentId": "1234-1234-1234-1234",
            "ErrorCode": None,
            "PaymentURL": "http://example.com/",
            "Message": None,
            "Details": None,
        }

    def test(self, api):
        responses.add(
            responses.GET,
            "https://securepay.tinkoff.ru/v2/Init",
            json={
                "Success": True,
                "PaymentId": "1234-1234-1234-1234",
                "ErrorCode": None,
                "PaymentURL": "http://example.com/",
                "Message": None,
                "Details": None,
            },
        )

        result = api.init_payment(
            amount_rub=100.0,
            order_id="1234",
            ip="1.1.1.1",
            description="Lorem ipsum dolro sit amet",
            lang="ru",
            notification_url="https://mysite.ru/notify/",
            success_url="https://mysite.ru/success/",
            fail_url="https://mysite.ru/fail/",
            pay_type="O",
            items=[
                TinkoffOrderItem(
                    name="Subject 1",
                    quantity=2,
                    amount_rub=25.0,
                    price_rub=10.0,
                    tax="none",
                    payment_method="full_payment",
                    payment_object="commodity",
                ),
                TinkoffOrderItem(
                    name="Subject 2",
                    quantity=1,
                    amount_rub=50.0,
                    price_rub=30.0,
                    tax="none",
                    payment_method="full_payment",
                    payment_object="commodity",
                ),
            ],
            client_email="client@example.com",
            client_phone="+71231231212",
            taxation="osn",
        )

        assert result.is_success
        assert result.payment_id == "1234-1234-1234-1234"
        assert result.error_code is None
        assert result.payment_url == "http://example.com/"
        assert result.message is None
        assert result.details is None
