from django.urls import path

from . import views

urlpatterns = [
    path("", views.DebugOrderView.as_view(), name="debug_order"),
    path("tinkoff/", views.TinkoffOrderView.as_view(), name="tinkoff_order"),
]
