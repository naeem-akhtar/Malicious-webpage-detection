# DEBUG = True
DEBUG = False

# TESTING = True
TESTING = False

# training dataset name
training_file_name = 'training_lexical_dataset'

# model classifier name (pickle file)
model_name = 'lexical_classifier'

# training password
training_psswd = '1913'
# % complete, urls done, time
training_status = []

# suspicious top-level-domain and words
Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk']
Suspicious_Words = ['secure','account','update','banking','login','click','confirm','password','verify','signin','ebayisapi','lucky','bonus']

# do not disturb the order of features
lexical_feature = ['blacklisted', 'IP_present', 'url_length', 'dots_in_url', 'domain_length', 'number_of_domains',\
    'hyphen_count_in_domain', 'digits_count_in_domain', 'largest_domain_length', 'avg_domain_length', 'directory_length', \
    'sub_directory_count', 'largest_directory_length', 'avg_directory_length', 'suspicious_TLD', \
    'file_name_length', 'dots_file_name', 'delims_file_name', 'argument_length', \
    'number_of_arguments', 'largest_arg_length', 'max_delims_in_args']

host_based_features = ['created_days_ago', 'updated_days_ago', 'expiration_days_remain', 'zipcode']

features_name = lexical_feature + [] + ['label']
