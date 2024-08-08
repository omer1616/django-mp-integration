from django.core.exceptions import ObjectDoesNotExist

from .models import Order
from .serializers import OrderSerializer, OrderItemSerializer


class OrderService:

    def create_order_with_order_items(self, item_data, order_data):

        order_instance = self.create_order(order_data)
        if order_instance:
            self.create_order_item(item_data, order_instance)

    def get_or_create_order(self, order_data):
        instance = None
        try:
            instance = Order.objects.get(**order_data)

        except ObjectDoesNotExist:
            serializer = OrderSerializer(data=order_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance = serializer.instance
        return instance

    def create_order_item(self, item_data, order_instance):
        for item in item_data:
            item.update({"order": order_instance})
        serializer = OrderItemSerializer(data=item_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

