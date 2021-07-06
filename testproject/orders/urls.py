from django.urls import path

from . import views

urlpatterns = [
    path("", views.DebugOrderView.as_view(), name="debug_order"),
    path("tinkoff/", views.TinkoffOrderView.as_view(), name="tinkoff_order"),
    path("payeer/", views.PayeerOrderView.as_view(), name="payeer_order"),
    path(
        "free_kassa/",
        views.FreeKassaOrderView.as_view(),
        name="free_kassa_order",
    ),
    path(
        "perfect_money/",
        views.PerfectMoneyOrderView.as_view(),
        name="perfect_money_order",
    ),
    path(
        "coinpayments/",
        views.CoinPaymentsOrderView.as_view(),
        name="coinpayments_order",
    ),
    path("qiwi/", views.QiwiOrderView.as_view(), name="qiwi_order"),
]
