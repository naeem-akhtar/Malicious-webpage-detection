from flask import Flask, current_app
from blinker import Namespace
from Prepare_training_dataset import extract_training_data
import time

app = Flask(__name__)


my_signals = Namespace()


def start_training(app, message, **extra):
    extract_training_data()
    # print(message)

train = my_signals.signal('train')
train.connect(start_training, app)


@app.route('/', methods=['POST', 'GET'])
def home():
    train.send(current_app._get_current_object(), message='Hi')
    return 'toot'


if __name__ == '__main__':
    app.run(debug=True, port=5002)
