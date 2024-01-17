from django.contrib import admin

from orders.models import Order, OrderItem, Table, OrderComment


class OrderItemInLine(admin.TabularInline):
    model = OrderItem

class CommentInline(admin.TabularInline):
    model = OrderComment

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["table", "time_created", "status",
                    "total_price", "is_takeaway", "payment"]
    list_filter = ["status", "total_price", "time_created", "table"]
    inlines = [OrderItemInLine, CommentInline]


admin.site.register(Table)
