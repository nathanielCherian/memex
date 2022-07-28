from requests.exceptions import ConnectionError
from memex.auth import gen_token
from memex.config import read_config
from memex.api import app
import json
import pytest

port = read_config()["DEFAULT"]["API_PORT"]
url = f"http://localhost:{port}/"
headers = {"content-type": "application/json"}

client = app.test_client()

def post_request(path, token, payload={}):
    headers["memex-token"] = token
    res_text = client.post(path,json=payload, headers=headers)
    return json.loads(res_text.data)



@pytest.fixture
def token():
    token = gen_token("foo")
    return token

def test_token(token):
    res = post_request('test-token', token)
    assert res['status'] == True


def test_create(token):
    obj = {
        "url": "http://example.com",
        "keywords": "test, test2",
    }
    res = post_request('/', token, payload=obj)
    assert res["url"] == obj["url"] and res["keywords"] == "test, test2"
