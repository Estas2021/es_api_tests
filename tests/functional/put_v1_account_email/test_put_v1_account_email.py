import time

from api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from api_account.apis.login_api import LoginApi
from faker import Faker
import base64
import re


from json import (
    loads,
    JSONDecodeError,
)

def test_put_v1_account_email():

    # зарегать пользака на Dungeonmaster.ru
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    fake = Faker()      # экземпляр класса для генерации фейковых данных

    login = f'FAKER_23_{fake.user_name()}'
    password = 'tester'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print("\nStatus_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 201, f"Error: user {login} hasn't been registered {response.json()}"


    # получить письмо из почтового ящика
    response = mailhog_api.get_api_v2_messages(response)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, "Error: message hasn't been delivered"


    # получить активационный токен на почтовом серве
    token = get_activation_token_by_login(login, response, f"Добро пожаловать на DM.AM, {login}!")
    print("Получение 1го активационного токена", token)
    assert token is not None, f"Error: token hasn't been delivered"


    # активировать пользака
    response = account_api.put_v1_account_token(token=token)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, f"Error: user {login} need to be activated!"


    # осуществить авторизацию
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, f"Error: user {login} can't authorize"


    # 1. сменить email

    json_data = {
        'login': login,
        'password': password,
        'email': email
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, "Error: email hasn't been changed"

    # 2. попытаться войти, получаем 403
    '''
    серверу может потребоваться время для обновления данных. Задержка позволяет убедиться,
    что данные актуальны перед следующим запросом.
    '''
    time.sleep(2)

    # 3. На почте найти токен по новому емейлу для подтверждения смены емейла

    token = get_activation_token_by_login(
        login, response, f'Подтверждение смены адреса электронной почты на DM.AM для {login}'
        )

    assert token is not None, f"Error: Token hasn't been received"

    # 4. активировать этот токен
    response = account_api.put_v1_account_token(token=token)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, f"Error: user {login} need to be activated!"


    # 5. авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print("Status_code: ", response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Error: user {login} can't be authorized. Step 5."
"""-----------------------------------------------------------------------------------------"""


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