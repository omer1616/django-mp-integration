from enumfields import Enum


class OrderStatus(Enum):

    HB_ORDER_STATUS = {

    }
    canceled = 'canceled'
    refunded = 'refunded'
    created = 'created'
    shipped = 'shipped'
    pending = 'pending'

