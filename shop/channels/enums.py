from enumfields import Enum


class ChannelType(Enum):
    hepsiburada = 'hepsiburada'
    ikas = 'ikas'


class ShippingCompany(Enum):
    aras = 'aras'
    yurtici = 'yurtici'
    mng = 'mng'
    hepsi_express = 'hbexpress'
