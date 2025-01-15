import requests
import pprint
from json import (
    loads,
    JSONDecodeError,
)


def test_user_registration_and_authorization():
    # 1) Рега пользака

    login = 'hunter3'
    password = 'tester'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print("\nStatus_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 201, f"Error: user hasn't been registered {response.json()}"


    # 2) Получить письма из почтового ящика

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print("Status_code: ", response.status_code)
    print("response.text: ", response.text)

    assert response.status_code == 200, "Error: messages haven't been delivered"

    # 3) Получить активационный токен
    token = None

    try:
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data.get('Login')
            if user_login == login:
                print('________login: ', user_login)
                token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
                print('_______token: ', token)
    except JSONDecodeError:
        print("Response is not a json format")
    except KeyError:
        print(f"There's no key USER_DATA")

    assert token is not None, f"Error: token hasn't been delivered for the user {login}"
    # test
    # for item in response.json()['items']:
    #     user_data = loads(item['Content']['Body'])
    #     user_login = user_data.get('Login')
    #     if user_login == login:
    #         print('login: ', user_login)
    #         token = user_data.get('ConfirmationLinkUrl').split('/')[-1]
    #         print('token: ', token)

    # 4) Активация пользака:

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}')
    print("Status_code: ", response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Error: user {login} hasn't been activated"

    # 5) Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post(f'http://5.63.153.31:5051/v1/account/login', json=json_data)

    print("Status_code: ", response.status_code)
    print(response.text)

    assert response.status_code == 200, f"Error: user {login} can't authorize"