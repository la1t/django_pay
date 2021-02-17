from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("orders.urls")),
    path("payments/", include("django_pay2.urls")),
    path("admin/", admin.site.urls),
]
