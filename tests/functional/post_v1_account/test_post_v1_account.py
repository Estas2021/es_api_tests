from faker import Faker
import base64
import re
import structlog
import json
from helpers.account_helpers import AccountHelper
from rest_client.configration import Configuration as MailhogConfiguration
from rest_client.configration import Configuration as EsApiConfiguration
from services.es_api_account import ESApiAccount
from services.api_mailhog import MailHogApi

from json import (
    loads,
    JSONDecodeError,
)

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

def test_post_v1_account():

    # зарегать пользака на Dungeonmaster.ru
    mailhog_configuration = MailhogConfiguration(
        host='http://5.63.153.31:5025',
        # disable_log=False
    )
    es_api_configuration = EsApiConfiguration(
        host='http://5.63.153.31:5051',
        disable_log=False
    )

    account = ESApiAccount(configuration=es_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(es_account_api=account, mailhog=mailhog)

    fake = Faker()      # экземпляр класса для генерации фейковых данных

    login = f'FAKER_33_{fake.user_name()}'
    password = 'tester'
    email = f'{login}@mail.ru'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.login_user(login=login, password=password)

print("---------------------------END------------------------------------------")

