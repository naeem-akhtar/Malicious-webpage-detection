import numpy as np
import pandas as pd
from Feature_Extraction import vector_construction
from global_variables import DEBUG

df_raw = pd.read_csv('final_dataset.csv', header=0)
if DEBUG:
    print(df_raw.head(5))

features_name = ['protocol', 'IP_present', 'url_length', 'dots_in_url', 'domain_length', 'number_of_domains',\
    'hyphen_count_in_domain', 'largest_domain_length', 'avg_domain_length', 'directory_length', \
    'sub_directory_count', 'largest_directory_length', 'avg_directory_length', 'suspicious_TLD', \
    'file_name_length', 'dost_file_name', 'delims_file_name', 'argument_length', \
    'number_of_arguments', 'largest_arg_length', 'max_delims_in_args', 'created_days_ago', \
    'updated_days_ago', 'expiration_days_remain', 'zipcode', 'label']
print('Number of Features :', len(features_name))

# Add columns to training dataset
df_training = pd.DataFrame(columns = features_name)

print('Extracting Training data from URL\'s')

# Add all features
i = 0
for url in df_raw['url']:
    df_training.loc[i] = vector_construction(url) + [df_raw['target']]
    i+=1
    if i >= 5:
        break

# delete raw dataframe 
del(df_raw)

# Add url and target columns
# df_training['url'] = df_raw.url
# df_training['target'] = df_raw.target

print('Extraction done')
if DEBUG:
    print(df_training.info())
    print(df_training.head(5))

print('dumping training data')

df_training.to_csv