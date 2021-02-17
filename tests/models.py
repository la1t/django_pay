import uuid

from django.db import models


class TestInvoice(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
