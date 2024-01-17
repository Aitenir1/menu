from django.urls import path, include

from dishes.views import DishListApi, CategoryListApi
from orders.views import OrderListApi, OrderCreateApi, OrderFilterListApi, OrderActiveListApi, OrderStatusUpdateApi, ReceiptPrintApi

app_name = "api"
urlpatterns = [
    path("dishes/", DishListApi.as_view(), name="dish_list"),
    path("categories/", CategoryListApi.as_view(), name="category_list"),
    path("orders/", OrderListApi.as_view(), name="order_list"),
    path("create-order/", OrderCreateApi.as_view(), name="order_create"),
    path("orders-filter/", OrderFilterListApi.as_view(), name="order_filter"),
    path("active-orders/", OrderActiveListApi.as_view(), name="active_orders"),
    path("orders/<str:pk>/status/", OrderStatusUpdateApi.as_view(), name='order_status'),
    path("print-receipt/", ReceiptPrintApi.as_view(), name="print_receipt")
]