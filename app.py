from sys import setrecursionlimit
from flask import Flask, request, jsonify, render_template, current_app
import logging
import prediction
from Prepare_training_dataset import extract_training_data
from global_variables import DEBUG

# needed to pickle blacklist
setrecursionlimit(5000)

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            url = request.form['url']
            state = 'malicious :(' if prediction.predict(url) else 'safe :)'
            # print(url, state)
        except:
            state = 'Error in cheking url.'
        return render_template('home.html', url_placeholder = url, state = state )
    elif request.method == 'GET':
        return render_template('home.html', url_placeholder = 'Enter your url here', state = '')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


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
    app.run(debug=True)


# for loggin output on logs of gunicorn / heroku
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
