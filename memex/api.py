import json
import logging

from flask import Flask, request

from memex.config import read_config
from memex.search import PowerSearch

from .auth import validate_token
from .entry import create_entry, find_entry, save_entry
from .utils import parse_token

app = Flask(__name__)


def handle_request(req, on_success, on_failure=lambda: ("Unauthorized", 401)):
    token = parse_token(request)
    status = validate_token(token, bearer=request.remote_addr)
    if status:
        return on_success(req)
    else:
        return on_failure()


@app.route("/", methods=["POST"])
def index():
    def success(req):
        req_json = req.json
        print("token authenticated")
        entry = create_entry(req_json)
        if not entry:
            return "Bad parameters", 400
        status = save_entry(entry)
        if not status:
            return "Unable to save entry", 500
        return entry.as_dict()

    if request.method == "POST":
        return handle_request(request, success)

    return


@app.route("/search", methods=["POST"])
def search():
    def success(req):
        try:
            req_json = req.json
            terms = req_json["terms"]
            operation = req_json["operation"]
            fields = ["keywords"]

            entries = PowerSearch(terms, operation, fields).execute()
            # entries = search_keywords_and(terms) if operation == 'and' else search_keywords_or(terms)

            return json.dumps(
                {
                    "entries": [entry.as_dict() for entry in entries],
                    "terms": terms,
                    "operation": operation,
                }
            )
        except Exception as e:
            return str(e), 500
        return

    if request.method == "POST":
        return handle_request(request, success)

    return


@app.route("/inspect", methods=["POST"])
def inspect():
    def success(req):
        try:
            req_json = req.json
            id_ = req_json["id"]
            entry = find_entry(id_)
            if entry is None:
                return "bad parameters", 400
            return json.dumps({"entry": entry.as_dict()})
        except Exception as e:
            return str(e), 500

    if request.method == "POST":
        return handle_request(request, success)
    return


@app.route("/test-token", methods=["POST"])
def test():
    def suc(x):
        return {"status": True}

    def fail():
        return {"status": False}

    if request.method == "POST":
        return handle_request(request, suc, on_failure=fail)
    return


def start_server():
    conf = read_config()
    app.run(debug=True, port=conf["DEFAULT"]["API_PORT"])


if __name__ == "__main__":
    start_server()
