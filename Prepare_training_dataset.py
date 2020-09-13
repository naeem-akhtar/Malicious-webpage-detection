import pandas as pd
import time
from global_variables import DEBUG, features_name, urls_file_name, training_file_name
from data_gathering import collect_urls_into_csv
from Feature_Extraction import vector_construction

# T1 >= T2
def calculate_time(T1, T2):
    t = T1-T2
    if t > 3600:
        return str(round(t/3600)) + ' hours'
    elif t > 60:
        return str(round(t/60)) + ' minutes'
    else:
        return str(round(t)) + ' seconds'


def extract_training_data():
    # Data collection from apis
    print('Collecting urls from apis(sources)')
    collect_urls_into_csv()

    df_urls = pd.read_csv(r'Dataset/' + urls_file_name + '.csv', header=0)
    if DEBUG:
        print(df_urls.head(5))

    print('Number of Features :', len(features_name))
    print('Features Name :', features_name)

    # Add columns to training dataset
    df_training = pd.DataFrame(columns = features_name)

    print('\nExtracting Training data from URL\'s. This might take a while :)')

    # Add all features
    i, percent = 0, 0
    start_time  = time.time()
    url_count = len(df_urls)
    for url in df_urls['url']:
        df_training.loc[i] = vector_construction(url) + [df_urls['target'].loc[i]]
        i += 1
        if (i*100)/url_count >= percent:
            percent += 1
            training_status = [round(i*100/url_count, 2), i, calculate_time(time.time(), start_time)]
            print('Extraction status : {0}% ({1}), time : {2}'.format(*training_status))
            # gunicorn logs
            # app.logger.info('Extraction status : {0}% ({1}), time : {2}'.format(*training_status))

    # delete raw dataframe 
    del(df_urls)

    print('Extraction done')
    if DEBUG:
        print(df_training.info())
        print(df_training.head(5))


    df_training.to_csv('./Dataset/' + training_file_name + '.csv', index=False)
    print('Training data is dumped as csv.\n')


if __name__ == '__main__':
    extract_training_data()
