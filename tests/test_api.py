from requests.exceptions import ConnectionError
from memex.auth import gen_token
from memex.config import read_config
import requests
import json
import pytest

port = read_config()['DEFAULT']['API_PORT']
url = f'http://localhost:{port}/'
headers = {'content-type': 'application/json'}

@pytest.fixture
def token():
    token = gen_token('foo')
    return token

def is_open():
    try:
        x = requests.head(url)
    except ConnectionError as e:
        raise Exception("run api before proceeding with tests...`")  

def test_token(token):
    headers['memex-token'] = token
    x = requests.post(url+'test-token', headers=headers)
    res = json.loads(x.content)
    assert res['status'] == True

def test_create(token):
    headers['memex-token'] = token
    obj = {
        'url':'http://example.com',
        'keywords':'test, test2',
    }
    x = requests.post(url, json=obj, headers=headers)
    res = json.loads(x.content)
    assert res['url'] == obj['url'] and res['keywords'] == 'test, test2'

