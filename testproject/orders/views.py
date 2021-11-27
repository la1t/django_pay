from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views import generic

from django_pay2 import create_payment

from .forms import OrderForm
from .models import Order


class PayeerOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            amount=amount,
            receiver=order,
            payment_system_name="payeer",
            desc=desc,
            currency="USD",
        )
        return redirect(payment_method.url)


class FreeKassaOrderView(generic.FormView):
    template_name = "orders/form_order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            amount=amount, receiver=order, payment_system_name="free_kassa"
        )
        return JsonResponse(
            {
                "action": payment_method.action,
                "fields": {key: value for key, value in payment_method.fields.items()},
            }
        )


class PerfectMoneyOrderView(generic.FormView):
    template_name = "orders/form_order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            request=self.request,
            amount=amount,
            receiver=order,
            currency="USD",
            payment_system_name="perfect_money",
        )
        return JsonResponse(
            {
                "action": payment_method.action,
                "fields": {key: value for key, value in payment_method.fields.items()},
            }
        )


class CoinPaymentsOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            amount=amount,
            receiver=order,
            payment_system_name="coinpayments",
            request=self.request,
            buyer_email="client@example.com",
            currency="ETH",
        )
        return redirect(payment_method.url)


class QiwiOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            amount=amount,
            receiver=order,
            currency="RUB",
            payment_system_name="qiwi",
        )
        return redirect(payment_method.url)


class QiwiKassaOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payment(
            amount=amount,
            receiver=order,
            currency="RUB",
            payment_system_name="qiwi_kassa",
        )
        return redirect(payment_method.url)
