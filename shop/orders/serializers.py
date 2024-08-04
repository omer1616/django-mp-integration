from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'status', 'sku', 'barcode', 'product_name', 'remote_order_item_id', 'extra_field']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'channel', 'customer', 'status', 'extra_field', 'order_items']
        read_only_fields = ['id']

