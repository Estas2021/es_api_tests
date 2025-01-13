"""
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "sefremov",
  "email": "stasefr2021@gmail.com",
  "password": "sefremov"
}'

curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/83e720c1-4f80-4de8-b26e-64268ba398e9' \
  -H 'accept: text/plain'
"""
import  requests
import pprint

# REGISTER USER
# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "sefremov",
#     "email": "stasefr2021@gmail.com",
#     "password": "sefremov"
# }
# response = requests.post(
#     url=url,
#     headers=headers,
#     data=json
# )
#
# # print(response.status_code)
# pprint.pprint(response.json())

# ACTIVATE USER
url = 'http://5.63.153.31:5051/v1/account/83e720c1-4f80-4de8-b26e-64268ba398e9'
headers = {
    'accept': '*/*',
}

response = requests.put(
    url=url,
    headers=headers,
)

print(response.status_code)
response_json = response.json()
pprint.pprint(response.json())
print(response_json['resource']['rating']['quantity'])