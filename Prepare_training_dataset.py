import pandas as pd
from global_variables import DEBUG, features_name, training_file_name
from data_gathering import collect_urls_into_csv
from Feature_Extraction import vector_construction

# Data collection from apis
print('Collecting urls from apis(sources)')
collect_urls_into_csv()

df_urls = pd.read_csv(r'Dataset/' + 'final_urls_dataset.csv', header=0)
if DEBUG:
    print(df_urls.head(5))

print('Number of Features :', len(features_name))

# Add columns to training dataset
df_training = pd.DataFrame(columns = features_name)

print('\nExtracting Training data from URL\'s. This might take a while :)')

# Add all features
i, j, = 0, 0
url_count = len(df_urls)
for url in df_urls['url']:
    df_training.loc[i] = vector_construction(url) + [df_urls['target'].loc[i]]
    i += 1
    if i%1000 == 0:
        print('Extraction status : {0}% ({1}/{2})'.format(round(i*100/url_count, 2), i, url_count))


# delete raw dataframe 
del(df_urls)

print('Extraction done')
if DEBUG:
    print(df_training.info())
    print(df_training.head(5))


df_training.to_csv('/Dataset/' + training_file_name + '.csv', index=False)
print('Training data is dumped as csv.\n')

