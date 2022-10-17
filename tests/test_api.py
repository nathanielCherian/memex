import pytest

from memex.auth_manager import AuthManager

from .utils import post_request


# Generates a token to be used in the rest of tests
@pytest.fixture
def token():
    token = AuthManager().gen_token("foo")
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


# def test_search(token):
#     obj = {"operation": "or", "terms": ["test"], "fields": ["keywords"]}
#     res = post_request("/search", token, payload=obj)
#     assert type(res["entries"]) == list
