import uuid

from django.db import models


class Table(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = "table"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"])
        ]

    def __str__(self):
        return f"Table #{self.id}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"

    def __str__(self):
        return f"{self.name}"


class OrderComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey('Order', related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(default='')

    def __str__(self):
        return f"{self.body}"

    class Meta:
        db_table = 'order_comment'


class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    TAKEAWAY_CHOICES = (
        (0, 'Here'),
        (1, 'Takeaway order'),
    )

    PAYMENT_CHOICES = (
        (0, 'Cash'),
        (1, 'Terminal')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    table = models.ForeignKey('Table', on_delete=models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_takeaway = models.IntegerField(choices=TAKEAWAY_CHOICES, default=0)
    payment = models.IntegerField(choices=PAYMENT_CHOICES, default=0)
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, editable=False)

    def __str__(self):
        return f"This order | {self.total_price}"

    class Meta:
        db_table = "order"
        ordering = ['status', 'time_created']


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dish = models.ForeignKey("dishes.Dish", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additives = models.ManyToManyField("dishes.Additive", blank=True)

    class Meta:
        db_table = "order_item"
