import requests

url = 'http://localhost:3000'
headers = {'content-type': 'application/json',
           'memex-token':'6de50430-e776-41eb-9605-8c43c671cf34'}
obj = {
    'url':'http://example.com',
    'keywords':'test'
}

x = requests.post(url, json=obj, headers=headers)

print(x)