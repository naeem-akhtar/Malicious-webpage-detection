# DEBUG = True
DEBUG = False

# TESTING = True
TESTING = False

# urls file name
urls_file_name = 'test_urls_1'

# training dataset name
training_file_name = 'test_dataset_1'

# model classifier name (pickle file)
# rmeove classifier name suffix from here while training
model_name = 'test_classifier_3_decision_tree'

# training password
training_psswd = '1913'
# % complete, urls done, time
training_status = []

# suspicious top-level-domain and words
Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk']
Suspicious_Words = ['secure','account','update','banking','login','click','confirm','password','verify','signin','ebayisapi','lucky','bonus']

# do not disturb the order of features
lexical_feature = ['IP_present', 'url_length', 'dots_in_url', 'having_at_the_rate',\
    'having_double_slash', 'having_https', 'hyphen_in_domain', 'digits_in_domain', \
    'directory_length', 'largest_directory_length', 'suspicious_TLD', \
    'file_name_length', 'argument_length',]

host_based_features = ['created_days_ago', 'present_in_whois']

content_based_features = ['iframe_ext_url', 'anchor_tag_ext_url', 'favicon_ext_urls', 'object_ext_url']

features_name = \
    lexical_feature + \
    ['label']

# print(features_name)
