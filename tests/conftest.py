from pytest_factoryboy import register

from .factories import (
    TestInvoiceFactory,
    PaymentFactory,
    PaymentRedirectFactory,
    PaymentFormFactory,
)


register(TestInvoiceFactory)
register(PaymentFactory)
register(PaymentRedirectFactory)
register(PaymentFormFactory)
