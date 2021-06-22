import factory

from django_pay2.models import Payment

from .models import TestInvoice


class TestInvoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TestInvoice


class PaymentFactory(factory.django.DjangoModelFactory):
    amount = 1000
    receiver = factory.SubFactory(TestInvoiceFactory)

    class Meta:
        model = Payment
