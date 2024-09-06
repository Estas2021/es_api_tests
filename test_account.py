import pytest
from faker import Faker
from client import Client


# @pytest.fixture
# def generate_user():
#     fake = Faker("ru_RU")
#     return {
#         "login": fake.user_name(),
#         "email": fake.email(),
#         "password": fake.password(),
#     }

@pytest.fixture
def client():
    return Client()


fake = Faker("ru_RU")
data = [

    # логин с 1 символом
    {
        "login": 'l',
        "email": fake.email(),
        "password": fake.password(),
    },
    # email с 1 символом
    {
        "login": fake.user_name(),
        "email": 'e',
        "password": fake.password(),
    },
    # password с 1 символом
    {
        "login": fake.user_name(),
        "email": fake.email(),
        "password": 'p',
    },
]

"""
Было до класса Клиент
@pytest.fixture
def set_url():
    return "http://5.63.153.31:5051"


@pytest.fixture
def set_headers():
    return {'accept': '*/*',
            'Content-Type': 'application/json'
            }
"""


@pytest.mark.parametrize('user_data', data)
def test_post_v1_account(user_data, client):
    response = client.register_user(user_data)
    # assert условие, сообщение об ошибке
    assert response.status_code == 200, "Status code must be 400"


"""
Научились:

1 генерить код с помощью постмана.
2 генерить тестовые фейковые данные с библой фейкер.
3 делать фикстуры(функции) для подготовки тестовых данных и окружений перед запуском теста.
4 параметризовывать тесты с разными данными.
5 делать ассерты.
"""
