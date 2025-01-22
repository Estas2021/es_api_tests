from api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from api_account.apis.login_api import LoginApi
from faker import Faker
import json
import base64
import re
from rest_client.configration import Configuration as MailhogConfiguration
from rest_client.configration import Configuration as EsApiConfiguration

from json import (
    loads,
    JSONDecodeError,
)

def test_put_v1_account_email():

    # зарегать пользака на Dungeonmaster.ru
    mailhog_configuration = MailhogConfiguration(
        host='http://5.63.153.31:5025',
        # disable_log=False
    )
    es_api_configuration = EsApiConfiguration(
        host='http://5.63.153.31:5051',
        disable_log=False
    )

    account_api = AccountApi(configuration=es_api_configuration)
    login_api = LoginApi(configuration=es_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    fake = Faker()      # экземпляр класса для генерации фейковых данных

    login = f'FAKER_22_{fake.user_name()}'
    password = 'tester'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)


    assert response.status_code == 201, f"Error: user {login} hasn't been registered {response.json()}"


    # получить письмо из почтового ящика
    response = mailhog_api.get_api_v2_messages(response)


    assert response.status_code == 200, "Error: message hasn't been delivered"


    # получить активационный токен на почтовом серве
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Error: token hasn't been delivered"


    # активировать пользака
    response = account_api.put_v1_account_token(token=token)


    assert response.status_code == 200, f"Error: user {login} need to be activated!"


    # осуществить авторизацию
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, f"Error: user {login} can't authorize"


    # 1. сменить email

    json_data = {
        'login': login,
        'password': password,
        'email': email
    }

    response = account_api.put_v1_account_email(json_data=json_data)


    assert response.status_code == 200, "Error: email hasn't been changed"

    # 2. попытаться войти, получаем 403

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 403, f"Error: user {login} can't be authorized. Step 2."

    # 3. На почте найти токен по новому емейлу для подтверждения смены емейла
    response = mailhog_api.get_api_v2_messages(response)

    assert response.status_code == 200, "Error: message hasn't been delivered"


    token = None

    def decode_mime(
            encoded_string: str
            ) -> str:
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

    # извлечь значение темы письма(Subject) из первого элемента списка items в response
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        subject_base64 = item["Content"]["Headers"]["Subject"][0]
        subject = decode_mime(subject_base64)
        substring = f'для {login}'
        if substring in subject:
            print('Тема письма для смены имейла: ', subject)
            token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
            print("Получение 2го активационного токена: ", token)


    # 4. активировать этот токен
    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, f"Error: user {login} need to be activated!"

    # token = get_activation_token_by_login(login, response)
    # print("token_2: ", token)
    #
    # assert token is not None, f"Error: token hasn't been delivered. Step 4."

    # 5. авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, f"Error: user {login} can't be authorized. Step 5."
"""-----------------------------------------------------------------------------------------"""

def get_activation_token_by_login(login, response):
    token = None
    try:
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data.get('ConfirmationLinkUrl').split('/')[-1]

    except JSONDecodeError:
        print("Response is not a json format")
    except KeyError:
        print(f"There's no key USER_DATA")

    return token