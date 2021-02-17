import uuid

from django.db import models


class Order(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    desc = models.TextField("Описание")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.desc
