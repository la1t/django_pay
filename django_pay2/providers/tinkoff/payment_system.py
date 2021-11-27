from typing import List, Optional

from django.urls import reverse
from ipware.ip import get_client_ip

from django.utils.translation import get_language
from django_pay2.exceptions import CreatePaymentError
from django_pay2.settings import payment_settings
from django_pay2.payment_methods import PaymentRedirect
from django_pay2.providers.base import PaymentSystem
from django_pay2.providers import register
from django_pay2.payment_methods import PaymentMethodType
from uuid import UUID
from decimal import Decimal as D

from .api import TinkoffOrderItem, TinkoffApiError
from .services import get_tinkoff_api


@register
class Tinkoff(PaymentSystem):
    name = "tinkoff"
    verbose_name = "Тинькофф"
    method_type = PaymentMethodType.REDIRECT

    def generate_payment_method(
        self,
        payment_id: UUID,
        amount: D,
        request,
        desc,
        items: List[TinkoffOrderItem],
        client_email: Optional[str] = None,
        client_phone: Optional[str] = None,
        **kwargs
    ):
        try:
            api = get_tinkoff_api()
            notification_url = reverse("django_pay2:tinkoff:notify")
            success_url = payment_settings.TINKOFF.return_url
            fail_url = payment_settings.TINKOFF.fail_url
            result = api.init_payment(
                amount,
                str(payment_id),
                get_client_ip(request)[0],
                desc,
                get_language(),
                notification_url,
                success_url,
                fail_url,
                items=items,
                client_email=client_email,
                client_phone=client_phone,
                email_company=payment_settings.TINKOFF.email_company,
                taxation=payment_settings.TINKOFF.taxation,
            )
            return PaymentRedirect(result.payment_url)
        except TinkoffApiError as exc:
            raise CreatePaymentError(str(exc))
