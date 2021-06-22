from pytest_factoryboy import register

from .factories import TestInvoiceFactory, PaymentFactory


register(TestInvoiceFactory)
register(PaymentFactory)
