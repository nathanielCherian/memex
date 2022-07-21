import requests

url = 'http://localhost:3000'
headers = {'content-type': 'application/json',
           'memex-token':'53cbff44-ddbb-4e10-ab45-662dcfbf0243'}
obj = {
    'url':'http://example.com',
    'keywords':'test',
}

x = requests.post(url, json=obj, headers=headers)

print(x)
print(x.content) 


# def _test_api():
    