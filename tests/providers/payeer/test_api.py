from decimal import Decimal

import factory
import pytest

from django_pay2.models import Payment
from django_pay2.providers.payeer.api import PayeerApi
from django_pay2.providers.payeer.exceptions import AlreadyPaid, PayeerValidationError
from tests.models import TestInvoice

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_uid():
    return "9234e6e7-d737-40f8-8fd3-e876116aab0b"


@pytest.fixture
def sample_sign():
    return "D018B2707E9DE7C6FAC75C00FFF9BFED8AFA6036473C58CD433B80194E88AD09"


@pytest.fixture
def api():
    return PayeerApi(
        account="qwerty",
        api_id="qwerty",
        api_password="qwerty",
        shop_id="qwerty",
        secret_key="qwerty",
    )


@pytest.fixture
def invoice():
    return TestInvoice.objects.create()


@pytest.fixture
def notify_data_factory(sample_uid, sample_sign):
    class NotifyDataFactory(factory.Factory):
        m_operation_id = 1
        m_operation_ps = 1
        m_operation_date = "2020-01-01"
        m_operation_pay_date = "2020-01-01"
        m_shop = "123456"
        m_orderid = sample_uid
        m_amount = Decimal("10.00")
        m_curr = "USD"
        m_desc = "Lorem ipsum dolor sit amet"
        m_status = "success"
        m_sign = sample_sign

        class Meta:
            model = dict

    return NotifyDataFactory


class TestPayeerApiNotify:
    def test_raise_err_if_data_is_empty(self, api):
        with pytest.raises(PayeerValidationError):
            api.notify({})

    def test_raise_err_if_there_are_no_such_payment(self, api, notify_data_factory):
        with pytest.raises(PayeerValidationError):
            api.notify(notify_data_factory())

    def test_raise_err_if_already_paid(
        self, payment_factory, invoice, sample_uid, api, notify_data_factory
    ):
        payment = payment_factory(
            status=Payment.StatusType.SUCCESS, receiver=invoice, id=sample_uid
        )

        with pytest.raises(AlreadyPaid):
            api.notify(notify_data_factory(order_id=str(payment.id)))

    def test_raise_err_if_amounts_are_not_equal(
        self, payment_factory, invoice, sample_uid, api, notify_data_factory
    ):
        payment = payment_factory(receiver=invoice, id=sample_uid)

        with pytest.raises(PayeerValidationError):
            api.notify(notify_data_factory(order_id=str(payment.id), amount=200))

    def test_raise_err_if_sign_is_incorrect(self, api, notify_data_factory):
        with pytest.raises(PayeerValidationError):
            api.notify(notify_data_factory(sign="incorrect"))

    def test_positive(
        self, notify_data_factory, payment_factory, invoice, sample_uid, api
    ):
        payment = payment_factory(receiver=invoice, id=sample_uid, amount=10)

        result = api.notify(notify_data_factory())

        assert str(result.payment.id) == payment.id
        assert result.status == "success"
        assert result.raw_order_id == sample_uid
