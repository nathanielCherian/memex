from flask import Flask, request
from memex.auth import validate_token
from memex.entry import create_entry, save_entry

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    if request.method == 'POST' :
        token = request.headers.get('memex-token', '')
        status = validate_token(token)
        if(status):
            print("TOKEN AUTHENTICATED...")
            print(request.json)
            url = request.json['url']
            keywords = request.json['keywords']
            entry = create_entry(url=url, keywords=keywords)
            if not entry: return 'Bad parameters', 400
            status = save_entry(entry)
            if not status: return 'Unable to save entry', 500
            return entry.as_dict()
        else:
            print('TOKEN NOT AUTHENTICATE.')

        print(request.headers.get('memex-token'))
        return {'status':status}

    return {'hi':'there'}

if __name__ == "__main__":
    app.run(debug=True, port=3000)
