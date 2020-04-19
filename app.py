from flask import Flask, request, jsonify
import prediction
from global_variables import DEBUG


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Go to predict page for checking the state of an url using POST request.'


@app.route('/predict', methods=['POST'])
def predict():
    try:
        try:
            url = request.json['url']
        except:
            return jsonify(description = 'wrong url format.')
        is_malicious = prediction.predict(url)
        # print(data.items())
        return jsonify(state = int(is_malicious), description = 'malicios :(' if is_malicious else 'safe :)')
    except:
        return jsonify(description = 'Error in checking this url.')


if __name__ == '__main__':
    app.run(debug=DEBUG)
