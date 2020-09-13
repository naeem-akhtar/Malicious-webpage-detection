import pickle
from Feature_Extraction import vector_construction
from Blacklist import blacklist
from global_variables import model_name, TESTING


classifier = pickle.load(open('Dataset/' + model_name + '.pkl', 'rb'))
print(model_name, classifier)

# malicious level = {0:safe, 1:predicted malicious by ML, 2:blacklisted}
def predict(url):
  # If present in blacklist
  if blacklist.find_url(url):
      return 2
  # either return 0 or 1
  is_malicious = classifier.predict([vector_construction(url)])
  return is_malicious[0]


if TESTING:
  print(predict(input()))
