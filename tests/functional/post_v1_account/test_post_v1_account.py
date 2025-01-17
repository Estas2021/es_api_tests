from api_account.apis.account_api import AccountApi
from api_mailhog.apis.mailhog_api import MailhogApi
from api_account.apis.login_api import LoginApi

from json import (
    loads,
    JSONDecodeError,
)


def test_user_registration_and_authorization():
    # 1) Рега пользака

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'hunter16.01'
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

    assert response.status_code == 201, f"Error: user hasn't been registered {response.json()}"


    # 2) Получить письма из почтового ящика

    response = mailhog_api.get_api_v2_messages(response)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, "Error: message hasn't been delivered"

    # 3) Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Error: token hasn't been delivered for the user {login}"
    # test
    # for item in response.json()['items']:
    #     user_data = loads(item['Content']['Body'])
    #     user_login = user_data.get('Login')
    #     if user_login == login:
    #         print('login: ', user_login)
    #         token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
    #         print('token: ', token)

    # 4) Активация пользака

    response = account_api.put_v1_account_token(token=token)
    print("Status_code: ", response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Error: user {login} hasn't been activated"

    # 5) Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print("Status_code: ", response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Error: user {login} can't authorize"

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





