from flask import Flask, request
from .auth import validate_token
from .entry import create_entry, create_from_dict, save_entry
from .utils import parse_token

app = Flask(__name__)

def handle_request(req, on_sucess, on_failure):
    token = parse_token(request)
    status = validate_token(token)
    if status:
        return on_sucess(req.json)
    else:
        return on_failure()


@app.route("/", methods=['POST'])
def index():

    def success(req_json):
        print("token authenticated")
        entry = create_from_dict(req_json)
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
    if request.method == 'POST':
        return handle_request(request, lambda: {'status':True}, lambda: {'status':False})
    return

def start_server():
    app.run(debug=True, port=3000)

if __name__ == "__main__":
    start_server()
