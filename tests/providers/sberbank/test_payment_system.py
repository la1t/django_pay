from decimal import Decimal as D

import pytest

from django_pay2.models import Payment
from django_pay2.providers.sberbank.payment_system import Sberbank

pytestmark = pytest.mark.django_db


class TestCreateSberbankPayment:
    @pytest.fixture
    def m_register_payment(self, mocker):
        return mocker.patch(
            "django_pay2.providers.sberbank.api.SberbankApi.register_payment"
        )

    def test_get_options_from_payment_settings(
        self, rf, test_invoice, m_register_payment
    ):
        Sberbank().create_payment(
            request=rf.get("/"),
            amount=12.12,
            desc="lorem ipsum",
            receiver=test_invoice,
            page_view="DESKTOP",
            phone="+71231231212",
        )

        assert Payment.objects.count() == 1
        payment = Payment.objects.get()
        assert payment.amount == D("12.12")
        assert payment.receiver == test_invoice
        m_register_payment.assert_called_once_with(
            order_num=str(payment.id),
            amount="12.12",
            return_url="return_url",
            fail_url="fail_url",
            description="lorem ipsum",
            page_view="DESKTOP",
            phone="+71231231212",
        )

    def test_get_options_from_args(self, rf, test_invoice, m_register_payment):
        Sberbank().create_payment(
            request=rf.get("/"),
            amount=12.12,
            desc="lorem ipsum",
            receiver=test_invoice,
            page_view="DESKTOP",
            phone="+71231231212",
            return_url="new_return_url",
            fail_url="new_fail_url",
        )

        assert Payment.objects.count() == 1
        payment = Payment.objects.get()
        assert payment.amount == D("12.12")
        assert payment.receiver == test_invoice
        m_register_payment.assert_called_once_with(
            order_num=str(payment.id),
            amount="12.12",
            return_url="new_return_url",
            fail_url="new_fail_url",
            description="lorem ipsum",
            page_view="DESKTOP",
            phone="+71231231212",
        )
