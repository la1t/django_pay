from django_pay2.contrib.rest_framework.serializers import (
    PaymentFormSerializer,
    PaymentRedirectSerializer,
)


def test_serialize_payment_redirect(payment_redirect_factory):
    redirect = payment_redirect_factory(url="https://example.com")

    serializer = PaymentRedirectSerializer(redirect)

    assert serializer.data["method"] == "redirect"
    assert serializer.data["url"] == "https://example.com"


def test_serializer_payment_form(payment_form_factory):
    form = payment_form_factory(
        action="https://example.com", fields__a="b", fields__b="c"
    )

    serializer = PaymentFormSerializer(form)

    assert serializer.data["method"] == "form"
    assert serializer.data["action"] == "https://example.com"
    assert serializer.data["fields"] == {"a": "b", "b": "c"}
