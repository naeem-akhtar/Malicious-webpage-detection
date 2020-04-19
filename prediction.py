import pickle
from Feature_Extraction import vector_construction
from global_variables import model_name, TESTING


classifier = pickle.load(open('Dataset/' + model_name + '.pkl', 'rb'))


def predict(url):
    is_malicious = classifier.predict([vector_construction(url)])
    return is_malicious[0]


if TESTING:
    print(predict(input()))
