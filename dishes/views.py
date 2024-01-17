from django.shortcuts import render
from django.utils import timezone
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .models import Category, Dish
from .serializers import CategorySerializer, DishSerializer


class CategoryListApi(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DishListApi(generics.ListAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

