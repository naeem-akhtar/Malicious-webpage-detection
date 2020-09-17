from sys import setrecursionlimit
from flask import Flask, request, jsonify, render_template, current_app
import logging
from ML_Framework.Prediction.prediction import predict as predict_ML

DEBUG = True

# needed to pickle blacklist, very high and unreliable
setrecursionlimit(10000)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            url = request.form['url']
            is_malicious = predict_ML(url)
            if is_malicious == 2:
                state = 'Blacklisted, very high potential to be malicious'
            elif is_malicious == 1:
                state = 'Predicted to be malicious :('
            else:
                state = 'Safe :)'
            # print(url, state)
        except:
            state = 'Error in cheking url.'
        return render_template('home.html', url_placeholder = url, state = state )
    elif request.method == 'GET':
        return render_template('home.html', url_placeholder = '', state = '')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        try:
            url = request.json['url']
        except:
            return jsonify(state = -1, description = 'wrong url format.')
        is_malicious = predict_ML(url)
        if is_malicious == 2:
            description = 'Blacklisted, very high potential to be malicious'
        elif is_malicious == 1:
            description = 'Predicted to be malicious :('
        else:
            description = 'Safe :)'
        # print(data.items())
        return jsonify(state = int(is_malicious), description = description)
    except:
        return jsonify(state = -1, description = 'Error in checking this url.')


if __name__ == '__main__':
    app.run(debug=True)


# for loggin output on logs of gunicorn / heroku
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
