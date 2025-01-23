from services.es_api_account import ESApiAccount
from services.api_mailhog import MailHogApi
import re
import base64
from json import (
    loads,
    JSONDecodeError,
)

from tests.functional.put_v1_account_token.test_put_v1_account_token import decode_mime


# ultra-mega FACADE which united 2 services: api_account & api_mailhog
class AccountHelper:

    def __init__(
            self,
            es_account_api: ESApiAccount,
            mailhog: MailHogApi
    ):
        # self.es_account_api = es_account_api
        self.es_account_api = es_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }

        response = self.es_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Error: user {login} hasn't been registered {response.json()}"

        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Error: registration email hasn't been delivered"

        token = self.get_activation_token_by_login(login=login, response=response, email_title=f"Добро пожаловать на DM.AM, {login}!")
        assert token is not None, f"Error: token hasn't been delivered"


        return response

    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        response = self.es_account_api.login_api.post_v1_account_login(json_data=json_data)

        assert response.status_code == 200, f"Error: user {login} can't authorize"

        return response

    @staticmethod
    def decode_mime(
            encoded_string
    ):
        """
        код предназначен для декодирования строки, закодированной в формате MIME (Multipurpose Internet Mail Extensions),
        который часто используется в электронной почте для кодирования не-ASCII символов.
        :param encoded_string:
        :return:
        """
        pattern = r"=\?utf-8\?b\?(.*?)\?="
        decoded_string = encoded_string

        for match in re.findall(pattern, encoded_string):
            decoded_part = base64.b64decode(match).decode("utf-8")
            decoded_string = decoded_string.replace(
                "=?utf-8?b?" + match + "?=", decoded_part
            )

        return decoded_string

    @staticmethod
    def get_activation_token_by_login(
            login,
            response,
            email_title
    ):
        token = None

        try:
            for item in response.json()['items']:
                user_data = loads(item['Content']['Body'])
                confirmation_condition = False
                if email_title:
                    decoded_email_title = decode_mime(item["Content"]["Headers"]["Subject"][0])
                    if email_title in decoded_email_title:
                        confirmation_condition = True
                user_login = user_data.get('Login')
                if user_login == login and email_title and confirmation_condition:
                    token = user_data.get('ConfirmationLinkUrl').split('/')[-1]

        except JSONDecodeError:
            print("Response is not a json format")
        except KeyError:
            print(f"There's no key USER_DATA")

        return token
