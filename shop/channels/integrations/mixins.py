import requests


class BaseIntegrationMixin:

    def __init__(self, channel_id, conf):
        self.channel_id = channel_id
        self.conf = conf

    def _send_request(self, url, method, auth, headers, **kwargs):
        try:
            response = requests.request(method=method, url=url, auth=auth, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Bir hata oluştu: {e}")
            return None

    def get(self, url, auth, **kwargs):
        return self._send_request(url=url, method="GET",
                                  auth=auth, **kwargs)

    def delete(self, url, auth, headers, **kwargs):
        return self.send_request(url=url, method='DELETE', auth=auth, headers=headers,
                                 **kwargs)

    def post(self, url, auth, headers, **kwargs):
        return self._send_request(url=url, method='POST', auth=auth, headers=headers,
                                  **kwargs)

    def put(self, url, auth, headers, **kwargs):
        return self._send_request(url=url, method='PUT', auth=auth, headers=headers,
                                  **kwargs)

    def patch(self, url, auth, headers, **kwargs):
        return self._send_request(url=url, method='PATCH', auth=auth, headers=headers,
                                  **kwargs)
