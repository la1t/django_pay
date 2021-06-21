from django.urls import path

from . import views

urlpatterns = [
    path("", views.DebugOrderView.as_view(), name="debug_order"),
    path("tinkoff/", views.TinkoffOrderView.as_view(), name="tinkoff_order"),
    path("payeer/", views.PayeerOrderView.as_view(), name="payeer_order"),
    path("payeer_1423418847.txt", views.confirm),
]
