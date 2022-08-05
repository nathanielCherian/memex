import json

import pytest
from requests.exceptions import ConnectionError

from memex.api import app
from memex.auth import gen_token


headers = {"content-type": "application/json"}

client = app.test_client()


def post_request(path, token, payload={}):
    headers["memex-token"] = token
    res_text = client.post(path, json=payload, headers=headers)
    print(res_text)
    return json.loads(res_text.data)


@pytest.fixture
def token():
    token = gen_token("foo")
    return token


def test_token(token):
    res = post_request("test-token", token)
    assert res["status"] == True


def test_create(token):
    obj = {
        "url": "http://example.com",
        "keywords": "test, test2",
    }
    res = post_request("/", token, payload=obj)
    assert res["url"] == obj["url"] and res["keywords"] == "test, test2"


def test_inspect(token):
    obj = {"id": 1}
    res = post_request("/inspect", token, payload=obj)
    assert type(res["entry"]) == dict


def test_search(token):
    obj = {"operation": "or", "terms": ["test"], 'fields':['keywords']}
    res = post_request("/search", token, payload=obj)
    assert type(res["entries"]) == list
