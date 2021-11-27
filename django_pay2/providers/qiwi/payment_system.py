from django_pay2.providers.base import PaymentSystem
from django_pay2.providers import register
from django_pay2.payment_methods import PaymentMethodType
from uuid import UUID
from decimal import Decimal as D
from django.utils import timezone
from datetime import timedelta

from .api import get_api


@register
class Qiwi(PaymentSystem):
    name = "qiwi"
    verbose_name = "Qiwi"
    method_type = PaymentMethodType.REDIRECT

    def generate_payment_method(
        self, payment_id: UUID, amount: D, currency, expirate_at=None, **kwargs
    ):
        expirate_at = expirate_at or timezone.now() + timedelta(hours=12)

        api = get_api()
        return api.generate_payment_method(amount, currency, expirate_at, payment_id)
