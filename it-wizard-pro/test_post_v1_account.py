import requests
import pprint

def test_user_registration_and_authorization():
    # 1) Рега пользака

    login = 'sefremov'
    password = 'tester'
    email = f'{login}'

    json_data = {
        'login': f'{login}',
        'email': f'{email}@mail.ru',
        'password': f'{password}',
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print("\nStatus_code: ", response.status_code)
    pprint.pprint((response.json()))

    # 2) Получить письма из почтового ящика

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print("Status_code: ", response.status_code)
    pprint.pprint((response.json()))

    # 3) Получить активационный токен
    pass
    # 4) Активация пользака

    response = requests.put('http://5.63.153.31:5051/v1/account/3b08bf34-206f-4d15-a726-6bf33ee662a6')
    print("Status_code: ", response.status_code)
    pprint.pprint((response.json()))

    # 5) Авторизоваться

    json_data = {
        'login': 'sefremov1',
        'password': 'sefremov1',
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)

    print("Status_code: ", response.status_code)
    pprint.pprint((response.json()))
