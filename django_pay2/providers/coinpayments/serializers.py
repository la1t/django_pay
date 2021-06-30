from rest_framework import serializers

from django_pay2.models import Payment


class CoinPaymentsApproveSerializer(serializers.Serializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())
    status = serializers.IntegerField()

    default_error_messages = {"not_done_status": "Not done status"}

    def validate_status(self, value):
        return value >= 100 or value == 2
