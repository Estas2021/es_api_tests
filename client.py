from requests import request


class Client():
    def __init__(self, host="http://5.63.153.31:5051", headers=None):
        self.host = host
        self.headers = headers or {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

    def register_user(self, json):
        path = self.host + '/v1/account'

        response = request(
            "POST",
            url=path,
            headers=self.headers,
            json=json
        )

        log = f"""
        REQUEST:
            URL: {response.request.url}
            METHOD: {response.request.method}
            JSON: {response.request.body}

        RESPONSE:
            STATUS_CODE: {response.status_code}
            CONTENT: {response.content}
        """
        print(log)
        return response
