import pytest
from pytest_factoryboy import register

from .factories import (
    PaymentFactory,
    PaymentFormFactory,
    PaymentRedirectFactory,
    TestInvoiceFactory,
)

register(TestInvoiceFactory)
register(PaymentFactory)
register(PaymentRedirectFactory)
register(PaymentFormFactory)


@pytest.fixture
def sample_uid():
    return "9234e6e7-d737-40f8-8fd3-e876116aab0b"
