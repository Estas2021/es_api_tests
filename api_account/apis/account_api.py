import requests

from rest_client.client import RestClient


class AccountApi(RestClient):

    # def __init__(
    #         self,
    #         host,
    #         headers=None
    # ):
    #     self.host = host
    #     self.headers = headers        # RestClient исп-ет такие же методы только логируемые


    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=json_data
        )
        return response


    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        response = self.put(
            path=f'/v1/account/{token}'
        )
        return response


    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=json_data
        )
        return response
