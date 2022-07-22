from flask import Flask, request
from memex.config import read_config
from .auth import validate_token
from .entry import create_entry, save_entry
from .utils import parse_token

app = Flask(__name__)

def handle_request(req, on_success, on_failure):
    token = parse_token(request)
    status = validate_token(token)
    if status:
        return on_success(req)
    else:
        return on_failure()


@app.route("/", methods=['POST'])
def index():
    def success(req):
        req_json = req.json
        print("token authenticated")
        entry = create_entry(req_json)
        if not entry: return 'Bad parameters', 400
        status = save_entry(entry)
        if not status: return 'Unable to save entry', 500
        return entry.as_dict()

    def failure():
        print("failed to authenticate token")
        return "Unauthorized", 401

    if request.method == 'POST' :
        return handle_request(request, success, failure)

    return

@app.route('/inspect', methods=['GET'])
def inspect():
    return 'Nope', 404

@app.route("/test-token", methods=['POST'])
def test():
    def suc(x):
        return {'status':True}
    def fail():
        return {'status':False}
    if request.method == 'POST':
        return handle_request(request, suc, fail)
    return

def start_server():
    conf = read_config()
    app.run(debug=True, port=conf['DEFAULT']['API_PORT'])

if __name__ == "__main__":
    start_server()
