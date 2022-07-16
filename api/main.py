from flask import Flask, request
from memex.auth import validate_token

app = Flask(__name__)

@app.route("/", methods=['POST'])
def index():
    if request.method == 'POST' :
        token = request.headers.get('memex-token', '')
        status = validate_token(token)
        if(status):
            print("TOKEN AUTHENTICATED...")
            print(request.json)
        else:
            print('TOKEN NOT AUTHENTICATE.')

        print(request.headers.get('memex-token'))
        return {'status':status}

    return {'hi':'there'}

if __name__ == "__main__":
    app.run(debug=True, port=3000)
