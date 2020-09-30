import pickle
from ML_Framework.utility.Feature_Extraction import vector_construction
from ML_Framework.utility.Blacklist import blacklist
from ML_Framework.utility.global_variables import model_name, TESTING

DATASET_MODELS_PATH = 'ML_Framework/Dataset/models/'

classifier = pickle.load(open(DATASET_MODELS_PATH + model_name + '.pkl', 'rb'))
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
	testing_url = 'https://www.google.com.naeemakhtar.com/path/end/here/virus.php'
	url = input("Enter Url or press enter to use testing url: ")
	print(predict(url))
