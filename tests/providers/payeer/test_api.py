from django_pay2.providers.payeer.exceptions import AlreadyPaid, PayeerValidationError
from django.test import TestCase

from django_pay2.providers.payeer.api import PayeerApi
from django_pay2.models import Payment

from tests.models import TestInvoice


class TestPayeerApiNotify(TestCase):
    sample_uid = "9234e6e7-d737-40f8-8fd3-e876116aab0b"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.api = PayeerApi(
            account="qwerty",
            api_id="qwerty",
            api_password="qwerty",
            shop_id="qwerty",
            secret_key="qwerty",
        )

    def setUp(self) -> None:
        self.invoice = TestInvoice.objects.create()

    def test_raise_err_if_data_is_empty(self):
        with self.assertRaises(PayeerValidationError):
            self.api.notify({})

    def test_raise_err_if_there_are_no_such_payment(self):
        with self.assertRaises(PayeerValidationError):
            self.api.notify(self.generate_data())

    def test_raise_err_if_already_paid(self):
        payment = self.create_payment(status=Payment.StatusType.SUCCESS)
        with self.assertRaises(AlreadyPaid):
            self.api.notify(self.generate_data(order_id=str(payment.id)))

    def test_raise_err_if_amounts_are_not_equal(self):
        payment = self.create_payment()

        with self.assertRaises(PayeerValidationError):
            self.api.notify(self.generate_data(order_id=str(payment.id), amount=200))

    def test_raise_err_if_sign_is_incorrect(self):
        self.create_payment()

        with self.assertRaises(PayeerValidationError):
            self.api.notify(self.generate_data(sign="incorrect"))

    def test_pass_validation(self):
        payment = self.create_payment()

        result = self.api.notify(self.generate_data())

        self.assertEqual(str(result.payment.id), payment.id)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.raw_order_id, self.sample_uid)

    def generate_data(
        self,
        order_id=sample_uid,
        amount="10.00",
        sign="D018B2707E9DE7C6FAC75C00FFF9BFED8AFA6036473C58CD433B80194E88AD09",
    ):
        return {
            "m_operation_id": "1",
            "m_operation_ps": "1",
            "m_operation_date": "2020-01-01",
            "m_operation_pay_date": "2020-01-01",
            "m_shop": "123456",
            "m_orderid": order_id,
            "m_amount": amount,
            "m_curr": "USD",
            "m_desc": "Lorem ipsum dolor sit amet",
            "m_status": "success",
            "m_sign": sign,
        }

    def create_payment(self, status=Payment.StatusType.PENDING):
        return Payment.objects.create(
            id=self.sample_uid, amount=10, receiver=self.invoice, status=status
        )
