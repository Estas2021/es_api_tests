from rest_client.configration import Configuration
from api_mailhog.apis.mailhog_api import MailhogApi


# общий фасад для удобства исп-я апишек или сервисов
class MailHogApi:

    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)
