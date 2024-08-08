import json
from django.db.transaction import atomic
from shop.orders.service import OrderService
from shop.channels.integrations.ikas.queries import Queries


class GetOrder:
    def __init__(self, integration, **kwargs):
        self.branch_id = kwargs.get('branchId')
        self.ordered_at = kwargs.get('orderedAt')
        self.pagination = kwargs.get('pagination')
        self.branch_session_id = kwargs.get('branchSessionId')
        self.customer_email = kwargs.get('customerEmail')
        self.customer_id = kwargs.get('customerId')
        self.id = kwargs.get('id')
        self.invoices_store_app_id = kwargs.get('invoicesStoreAppId')
        self.order_number = kwargs.get('orderNumber')
        self.order_package_status = kwargs.get('orderPackageStatus')
        self.order_payment_status = kwargs.get('orderPaymentStatus')
        self.order_tag_ids = kwargs.get('orderTagIds')
        self.payment_method_type = kwargs.get('paymentMethodType')
        self.sales_channel_id = kwargs.get('salesChannelId')
        self.search = kwargs.get('search')
        self.shipping_method = kwargs.get('shippingMethod')
        self.sort = kwargs.get('sort')
        self.status = kwargs.get('status')
        self.stock_location_id = kwargs.get('stockLocationId')
        self.terminal_id = kwargs.get('terminalId')
        self.updated_at = kwargs.get('updatedAt')

        self.variables = kwargs.get('variables')

        super.__init__(integration, **kwargs)

    @property
    def _request_body_token(self):
        grant_type = self.integration.conf.get('grant_type')
        client_id = self.integration.conf.get('client_id')
        client_secret = self.integration.conf.get('client_secret')
        body = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        return json.dumps(body)

    @property
    def _get_access_token(self):
        shop_url = self.integration.shop_url

        response = self.interation.post(shop_url, data=self._request_body_token)
        r = response.json()

        return f"{r.get('token_type')} {r.get('access_token')}"

    @property
    def _set_headers(self):
        self.integration.headers = {
            'Authorization': self._get_access_token,
            'Content-Type': 'application/json'
        }

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
            customer_name = order['customer'].get("firstName")
            customer_id = order['customer'].get("id")
            order_packages = order['orderPackages']
            if len(order_packages) == 1:
                package_number = order_packages[0].get("orderPackageNumber")
                barcode = order_packages[0].get("trackingInfo").get("barcode")
                cargo_company = self._get_cargo_company(order_packages[0].get("trackingInfo").get("cargoCompany"))
                generated_order_number = self._generate_order_number(channel_id, order_number, package_number)
            elif len(order_packages) > 1:
                for order_package in order_packages:
                    package_number = order_package.get("orderPackageNumber")
                    barcode = order_package.get("trackingInfo").get("barcode")
                    cargo_company = self._get_cargo_company(order_package.get("trackingInfo").get("cargoCompany"))
                    generated_order_number = self._generate_order_number(channel_id, order_number, package_number)

            order_status = self._get_order_status(order.get('orderPackageStatus'))

            items = order['orderLineItems']
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
                    'remote_item_id': item['id'],
                    'quantity': item['quantity'],
                    'sku': item['variant'].get('sku'),
                }
                item_data.append(item_data_dict)

            with atomic():
                service.create_order_with_order_items(
                    item_data=item_data,
                    order_data=order_data,
                )

    @property
    def _get_url(self):
        url = self.integration.base_url
        return url

    @property
    def _get_payload(self):
        payload = {
            'branchId': self.branch_id,
            'variables': self.variables,
            'query': Queries.ORDER_QUERY
        }
        return payload

    def run(self):
        response = self.send()
        if response.status_code == 200:
            self.process_response(self, response)

    def process_response(self, response):
        response_data = response.get('data').get("listOrder").get("data", [])
        self.create_orders(response_data)

    def send(self):
        response = self.integration.post(
            self._get_url,
            headers=self._set_headers,
            json=self._get_payload

        )

        return response
