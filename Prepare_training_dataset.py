import pandas as pd
from global_variables import DEBUG, features_name
from data_gathering import collect_urls_into_csv
from Feature_Extraction import vector_construction

# Data collection from apis
print('Collecting urls from apis(sources)')
collect_urls_into_csv()

df_raw = pd.read_csv('final_urls_dataset.csv', header=0)
if DEBUG:
    print(df_raw.head(5))

print('Number of Features :', len(features_name))

# Add columns to training dataset
df_training = pd.DataFrame(columns = features_name)

print('Extracting Training data from URL\'s \nThis might take a while :)\n')

# Add all features
i = 0
for url in df_raw['url']:
    df_training.loc[i] = vector_construction(url) + [df_raw['target'].loc[i]]
    i+=1
    if i >= 100:
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


df_training.to_csv('training_dataset.csv', index=False)

print('Training data is dumped as csv.')