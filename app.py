from flask import Flask, request, jsonify, render_template, current_app
from blinker import Namespace
import logging
import prediction
from Prepare_training_dataset import extract_training_data
from global_variables import DEBUG, training_psswd, training_status


app = Flask(__name__)

training_signals = Namespace()
def start_training(app, **extra):
    extract_training_data()


train = training_signals.signal('train')
train.connect(start_training, app)


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


@app.route('/training', methods=['POST'])
def training():
    if request.method == 'POST':
        try:
            password = request.json['password']
            if password == training_psswd:
                try:
                    # training of model start
                    train.send(current_app._get_current_object())
                    # training end
                    return jsonify(result = 'Prepared training database. ML Model can be trained.')
                except:
                    return jsonify(result = 'cannot prepare training dataset.')
            else:
                return jsonify(result = 'wrong password')
        except:
            return jsonify(result = 'cannot extract password')


if __name__ == '__main__':
    app.run(debug=True)


# for loggin output on logs of gunicorn / heroku
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
