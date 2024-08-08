from collections import OrderedDict
from shop.channels.integrations.mixins import BaseIntegrationMixin
from shop.channels.enums import ShippingCompany


from shop.orders.enums import OrderStatus
from .commands import GetOrder


class Integration(BaseIntegrationMixin):
    ikas_cargo_companies_mapping = {
        'Yurtiçi Kargo': ShippingCompany.yurtici,
        'Aras Kargo': ShippingCompany.aras,
        'Hepsi Express': ShippingCompany.hepsi_express,
        'MNG Kargo': ShippingCompany.mng,
    }
    ikas_order_status_mapping = {
        'FULFILLED': OrderStatus.created,
        'READY_FOR_PICK_UP': OrderStatus.packaged,
        'READY_FOR_SHIPMENT': OrderStatus.packaged,
        'CANCELLED': OrderStatus.canceled,
        'REFUNDED': OrderStatus.refunded,
        'DELIVERED': OrderStatus.delivery,
    }
    command_class = OrderedDict([
        ('get_order', GetOrder)

    ])

    @property
    def base_url(self):
        return self.conf.get("base_url", "https://api.myikas.com/api/v1/admin/graphql")

    @property
    def shop_url(self):
        return self.conf.get("shop_url",  "https://omer.myikas.com/api/admin/oauth/token")

    def do_action(self, key, **kwargs):
        action_class = self.command_class[key]
        action = action_class(**kwargs)
        if action:
            return action.run()
        return 0
