from urllib.parse import urlencode
from django.db.transaction import atomic
from shop.orders.models import Order
from shop.orders.serializers import OrderSerializer
from shop.orders.service import OrderService
from shop.channels.models import Channel


class GetOrder:

    def __init__(self, integration, **kwargs):
        self.limit = min(kwargs.get('limit', 10), 10)
        self.offset = kwargs.get('offset', 0)
        self.timespan = kwargs.get('timespan') or 1
        self.begin_date = kwargs.get('begin_date', None)
        self.end_date = kwargs.get('end_date', None)
        super.__init__(integration, **kwargs)

    @property
    def _get_request_data(self):
        username = self.integration.conf.get('username')
        password = self.integration.conf.get('password')

        return (username, password)

    def _get_cargo_company(self, key):
        if key:
            return self.integration.hb_cargo_companies_mapping[key]
        return None

    def _get_order_status(self, key):

        return self.integration.hb_order_status_mapping[key]

    def _generate_order_number(self, channel_id, order_number, package_number):

        return f"{channel_id}-{order_number}-{package_number}"

    def create_orders(self, order_data):
        channel_id = self.integration.channel_id
        service = OrderService()

        for order in order_data:
            order_remote_id = order['id']
            order_number = order['orderNumber']
            customer_name = order['orderNumber']
            customer_id = order['customerId']
            package_number = order['packageNumber']
            barcode = order['barcode']
            items = order['items']
            cargo_company = self._get_cargo_company(order.get('cargoCompany'))
            order_status = self._get_order_status(order.get('orderStatus'))
            generated_order_number = self._generate_order_number(channel_id, order_number, package_number)


            extra_data = {
                'barcode': barcode,
                'package_number': package_number,
                'cargo_company': cargo_company,
                'remote_id': order_remote_id,
            }
            order_data = {
                'channel_id': channel_id,
                'order_number': generated_order_number,
                'status': order_status,
                'extra_field': extra_data
            }

            item_data = []
            for item in items:
                item_data_dict = {
                    'remote_item_id': item['lineItemId'],
                    'quantity': item['quantity'],
                    'sku': item['hbSku'],
                    'barcode': item['productBarcode']}
                item_data.append(item_data_dict)

            with atomic():
                service.create_order_with_order_items(
                    item_data=item_data,
                    order_data=order_data,
                )

    def get_url(self):
        merchant_id = self.integration.conf.get('merchantId')
        url = f"{self.integration.base_url}/packages/merchantid/{merchant_id}"
        params = {
            'limit': self.limit,
            'offset': self.offset
        }

        if self.begin_date and self.end_date:
            params.update({
                'beginDate': self.begin_date,
                'endDate': self.end_date
            })
        else:
            params.update({
                'timespan': self.timespan
            })

        url += urlencode(params)

        return url

    def run(self):
        response = self.send()
        if response.status_code == 200:
            self.process_response(self, response)

    def process_response(self, response):
        self.create_orders(response)

    def send(self):
        response = self.integration.get(
            self.get_url(),
            auth=self._get_request_data
        )

        return response
