from django.contrib import admin

from dishes.models import Category, Dish, Additive

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Dish)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ru',
                    'price', 'available', 'is_trend']

    list_filter = ['available', 'is_trend', 'price']
    list_editable = ['price', 'available']


@admin.register(Additive)
class AdditiveAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ru',
                    'price', 'dish']
    list_filter = ['price', 'dish']
