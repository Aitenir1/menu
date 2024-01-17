import uuid
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return f"Category: {self.name}"


class Dish(models.Model):
    TREND_CHOINCES = (
        (0, 'Trend'),
        (1, 'Not trend')
    )

    AVAILABLE_CHOICES = (
        (0, "Available"),
        (1, "Unavailable"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200, default='Тамак')
    name_ru = models.CharField(max_length=200, default='Еда')
    description_en = models.TextField()
    description_kg = models.TextField(default='Тамак')
    description_ru = models.TextField(default='Еда')
    price = models.FloatField()
    gram = models.CharField(max_length=100, default='200')
    category = models.ForeignKey('Category',
                                 related_name="dishes", blank=True,
                                 null=True, on_delete=models.CASCADE)
    available = models.IntegerField(choices=AVAILABLE_CHOICES, default=0)
    image = models.ImageField(default='food1.png', upload_to='dishes/')
    is_trend = models.IntegerField(choices=TREND_CHOINCES, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        verbose_name_plural = "dishes"
        db_table = "dish"

    def __str__(self):
        return f"Dish: {self.name_en}"


class Additive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    name_kg = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='additives')

    class Meta:
        db_table = "additive"

    def __str__(self):
        return f"Additive for {self.dish.name_en}: {self.name_en}"
