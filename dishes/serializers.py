from rest_framework import serializers

from .models import Category, Additive, Dish

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class AdditiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additive
        fields = ["name_en", "name_ru", "name_kg", "price"]


class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    additives = AdditiveSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ['id', 'name_en', 'name_kg', 'name_ru',
                  'description_en', 'description_kg', 'description_ru',
                  'price', 'gram', 'category', 'available', 'image',
                  'is_trend', 'additives']
