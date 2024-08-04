from collections import OrderedDict

from shop.channels.integrations.mixins import BaseIntegrationMixin
from shop.channels.enums import ShippingCompany
from shop.channels.models import Channel
import requests
from .commands import GetOrder


class Integration(BaseIntegrationMixin):
    hb_cargo_companies = {
        'Yurtiçi Kargo': ShippingCompany.yurtici,
        'Aras Kargo': ShippingCompany.aras,
        'Hepsi Express': ShippingCompany.hepsi_express,
        'MNG Kargo': ShippingCompany.mng,
    }
    command_class = OrderedDict([
        ('get_order', GetOrder)

    ])

    @property
    def base_url(self):
        return self.conf.get("base_url", "https://mpop-sit.hepsiburada.com")

    def do_action(self, key, **kwargs):
        action_class = self.command_class[key]
        action = action_class(**kwargs)
        return action.run()
