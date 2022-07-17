import requests

url = 'http://localhost:3000'
headers = {'content-type': 'application/json',
           'memex-token':'d40c00cd-d595-4693-ac10-95a8a1290e29'}
obj = {
    'url':'http://example.com',
    'keywords':'test',
}

x = requests.post(url, json=obj, headers=headers)

print(x)
print(x.content)