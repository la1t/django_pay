import factory

from django_pay2.models import Payment
from django_pay2.payment_methods import PaymentRedirect, PaymentForm

from .models import TestInvoice


class TestInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TestInvoice


class PaymentFactory(factory.django.DjangoModelFactory):
    amount = 1000
    receiver = factory.SubFactory(TestInvoiceFactory)

    class Meta:
        model = Payment


class PaymentRedirectFactory(factory.Factory):
    url = "https://example.com"

    class Meta:
        model = PaymentRedirect


class PaymentFormFactory(factory.Factory):
    action = "https://example.com"
    fields = factory.SubFactory(factory.DictFactory)

    class Meta:
        model = PaymentForm
