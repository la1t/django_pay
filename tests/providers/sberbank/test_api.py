import pytest
import responses

from django_pay2.providers.sberbank.api import SberbankApi
from django_pay2.providers.sberbank.exceptions import SberbankApiError


@pytest.fixture
def api():
    return SberbankApi("username", "password")


class TestSberbankApiRegisterPayment:
    @responses.activate
    def test_return_payment_redirect_if_response_is_ok(self, api: SberbankApi):
        responses.add(
            responses.POST,
            "https://securepayments.sberbank.ru/payment/rest/register.do",
            json={"orderId": "123456", "formUrl": "https://example.com/formUrl/"},
        )
        method = api.register_payment(
            order_num="12345678",
            amount="123.12",
            return_url="https://example.com/return/",
            fail_url="https://example.com/fail/",
            description="lorem ipsum",
        )

        assert method.url == "https://example.com/formUrl/"
        assert len(responses.calls) == 1
        assert responses.calls[0].request.params == {
            "userName": "username",
            "password": "password",
            "orderNumber": "12345678",
            "amount": "123.12",
            "returnUrl": "https://example.com/return/",
            "failUrl": "https://example.com/fail/",
            "description": "lorem ipsum",
        }

    @responses.activate
    def test_raise_err_if_response_is_not_ok(self, api: SberbankApi):
        responses.add(
            responses.POST,
            "https://securepayments.sberbank.ru/payment/rest/register.do",
            status=400,
        )

        with pytest.raises(SberbankApiError):
            api.register_payment(
                order_num="12345678",
                amount="123.12",
                return_url="https://example.com/return/",
                fail_url="https://example.com/fail/",
                description="lorem ipsum",
            )

    @responses.activate
    def test_raise_err_if_response_has_error_code(self, api: SberbankApi):
        responses.add(
            responses.POST,
            "https://securepayments.sberbank.ru/payment/rest/register.do",
            json={"errorCode": "123", "errorMessage": "lorem ipsum"},
        )

        with pytest.raises(SberbankApiError):
            api.register_payment(
                order_num="12345678",
                amount="123.12",
                return_url="https://example.com/return/",
                fail_url="https://example.com/fail/",
                description="lorem ipsum",
            )
