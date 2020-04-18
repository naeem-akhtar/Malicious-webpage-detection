import pickle
from Feature_Extraction import vector_construction
from global_variables import model_name

classifier = pickle.load(open(r'./Dataset/' + model_name + '.pkl', 'rb'))

def predict(url):
    is_malicious = classifier.predict([vector_construction(url)])
    return is_malicious[0]


# print(predict(input()))