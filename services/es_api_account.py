from rest_client.configration import Configuration
from api_account.apis.account_api import AccountApi
from api_account.apis.login_api import LoginApi


# общий фасад для удобства исп-я апишек или сервисов
class ESApiAccount:

    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.login_api = LoginApi(configuration=self.configuration)
        self.account_api = AccountApi(configuration=self.configuration)
