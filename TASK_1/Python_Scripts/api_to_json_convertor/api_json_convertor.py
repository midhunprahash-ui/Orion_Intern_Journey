'''
curl -X 'GET' \
  'https://api.data.gov.in/resource/0cde42d3-5f49-4d2a-996c-4dfc4b2e2596?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json' \
  -H 'accept: application/json'

'''

import requests

api_endpoint = "https://api.data.gov.in/resource/0cde42d3-5f49-4d2a-996c-4dfc4b2e2596?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json"

response = requests.get(api_endpoint)
# print(response.content)

with open("api_to_json.json","w") as f:
    print(response.content)
    # f.write(requests.get(api_endpoint).content.decode())



'''
HTTP Methods - GET, POST, PUT, PATCH, DELETE

Status Codes - 1XX, 2XX, 3XX, 4XX, 5XX
'''