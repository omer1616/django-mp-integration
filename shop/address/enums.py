from enumfields import Enum


class AddressType(Enum):
    billing_address = 'billing_address'
    shipping_address = 'shipping_address'