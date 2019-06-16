from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def serve_part2():
    # get request arguments
    user_id = request.args.get('userid')
    n = request.args.get('n')

    # input validations
    if user_id is None:
        return "user id is invalid"
    if n is None:
        return "n is invalid"
    try:
        int(n)
    except Exception:
        return "n is not a number"

    highest_predictions = CALL_SHIRAS_FUNCTION(user_id, n)
    return highest_predictions


if __name__ == '__main__':
    print "web service is running"
    app.run(debug=True)
