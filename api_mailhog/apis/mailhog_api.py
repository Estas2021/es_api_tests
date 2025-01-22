import requests

from rest_client.client import RestClient


class MailhogApi(RestClient):
    #
    # def __init__(
    #         self,
    #         host,
    #         headers=None
    # ):
    #     self.host = host
    #     self.headers = headers

    def get_api_v2_messages(
            self,
            limit=50
    ):
        """
        Get user emails
        :return:
        """
        params = {
            'limit': limit,
        }

        response = self.get(
            path='/api/v2/messages',
            params=params,
            verify=False
        )
        return response
