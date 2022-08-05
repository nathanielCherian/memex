from ast import parse
import requests
import urllib.parse
import json

class MemexRemote:

    def __init__(self, url, token):
        self.endpoint = url
        self.token = token
        # load the remote url and token
        # check test-token exists
        pass

    def make_request(self, url, payload):
        headers = {"content-type": "application/json", 'memex-token':self.token}
        return requests.post(url, json=payload, headers=headers)

    def execute(self, path, args):
        url = urllib.parse.urljoin(self.endpoint, path)
        res = self.make_request(url, args)
        status_code = res.status_code
        if status_code == 401:
            print("Failed to authenticate token. Please regenerate token")
            exit()
        elif status_code == 400:
            print("Failed to run command on server. Bad parameters")
            exit()
        elif status_code == 500:
            print("Failed to run command on server. Check API")
            exit()

        json_res = json.loads(res.content)
        return json_res



if __name__ == "__main__":
    mr = MemexRemote('http://localhost:3000', 'd8e3dec6-47fe-4280-8855-b5ad8c174b7c')
    mr.execute('test-token', {})
    # x = mr.make_request(mr.url, mr.token)
    # print(x.status_code, x.content)