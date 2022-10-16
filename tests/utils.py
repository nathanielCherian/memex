import json
import os

from memex.api import app


def remove_db():
    dirname = os.path.dirname(__file__)
    os.remove(os.path.join(dirname, "example.db"))


# utility function to make a post request to the client
def post_request(path, token, payload={}):
    headers = {
        "content-type": "application/json",
        "memex-token": token,
    }
    res_text = app.test_client().post(path, json=payload, headers=headers)
    print(res_text)
    return json.loads(res_text.data)
