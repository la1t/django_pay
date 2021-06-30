from django.http.response import JsonResponse
from django_pay2.providers.free_kassa.create_payment import create_free_kassa_payment
from django.shortcuts import redirect
from django.views import generic

from django_pay2.providers.debug import create_debug_payment
from django_pay2.providers.tinkoff import create_tinkoff_payment
from django_pay2.providers.tinkoff.entities.init import Item
from django_pay2.providers.payeer import create_payeer_payment
from django_pay2.providers.perfect_money import create_perfect_money_payment

from .forms import OrderForm
from .models import Order


class DebugOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_debug_payment(
            self.request,
            amount,
            desc,
            order,
            client_email="client@example.com",
        )
        return redirect(payment_method.url)


class TinkoffOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        item = Item(
            "Test",
            1,
            amount,
            amount,
            "none",
        )
        payment_method = create_tinkoff_payment(
            self.request,
            amount,
            desc,
            order,
            [item],
            client_email="client@example.com",
        )
        return redirect(payment_method.url)


class PayeerOrderView(generic.FormView):
    template_name = "orders/order.html"
    form_class = OrderForm

    def form_valid(self, form):
        desc = form.cleaned_data["desc"]
        amount = form.cleaned_data["amount"]
        order = Order.objects.create(desc=desc)
        payment_method = create_payeer_payment(
            self.request,
            amount,
            desc,
            order,
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
        payment_method = create_free_kassa_payment(self.request, amount, desc, order)
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
        payment_method = create_perfect_money_payment(
            self.request, amount, desc, order, "USD"
        )
        return JsonResponse(
            {
                "action": payment_method.action,
                "fields": {key: value for key, value in payment_method.fields.items()},
            }
        )
