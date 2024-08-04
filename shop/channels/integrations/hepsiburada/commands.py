from urllib.parse import urlencode


class GetOrder:

    def __init__(self, integration, **kwargs):
        self.limit = min(kwargs.get('limit', 10), 10)
        self.offset = kwargs.get('offset', 0)
        self.timespan = kwargs.get('timespan') or 1
        self.begin_date = kwargs.get('begin_date', None)
        self.end_date = kwargs.get('end_date', None)
        super.__init__(integration, **kwargs)

    def get_request_data(self):
        username = self.integration.conf.get('username')
        password = self.integration.conf.get('password')

        return (username, password)

    def create_order(self, order_data):
        for order in order_data:
            pass

    def get_url(self):
        merchant_id = self.integration.conf.get('merchantId')
        url = f"{self.integration.url}/orders/merchantid/{merchant_id}"
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
            self.process_response(self)

    def process_response(self, response):
        self.create_order(response)

    def send(self):
        response = self.integration.get(
            self.get_url(),
            auth=self.get_request_data()
        )

        return response
