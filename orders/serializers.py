from rest_framework import serializers

from api.utils.order_create_logic import create_order_from_json
from dishes.models import Additive
from dishes.serializers import AdditiveSerializer, DishSerializer
from orders.models import OrderItem, OrderComment, Order

from api.utils.print_receipt import print_receipt


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderComment
        fields = ["body"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["dish", "quantity", "additives"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # comment = CommentSerializer(many=True)
    comment = serializers.CharField(required=False)
    time_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created',
                  'status', 'payment', 'is_takeaway',
                  'total_price', 'items', 'comment']

    def create(self, validated_data: dict):
        table = validated_data.pop('table')
        order_items = validated_data.pop('items')
        payment = validated_data.get('payment', 0)
        is_takeaway = validated_data.get('is_takeaway', 0)
        comment = validated_data.get('comment', '-')

        order = create_order_from_json(
            table=table,
            order_items=order_items,
            payment=payment,
            is_takeaway=is_takeaway,
            comment=comment
        )

        # print_receipt(
        #    customer=False,
        #    items=order_items,
        #    table=table,
        #    comment=comment
        #)

        return order

class OrderItemGetSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    additives = AdditiveSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'additives']


class OrderGetSerializer(serializers.ModelSerializer):
    items = OrderItemGetSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created', 'status', 'payment', 'is_takeaway', 'total_price', 'items', 'comments']
