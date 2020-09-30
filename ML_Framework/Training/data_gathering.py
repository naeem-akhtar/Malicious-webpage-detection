import pandas as pd
from sklearn.utils import shuffle

try:
    from ML_Framework.utility.global_variables import DEBUG, TESTING, urls_file_name
except:
    DEBUG = True
    TESTING = True
    urls_file_name = 'test_urls_1'

DATASET_CSVS_PATH = 'ML_Framework/Dataset/csvs/'

def benign_urls_api():
    urls =  pd.read_csv(DATASET_CSVS_PATH + 'filtered_benign.csv')['url']
    return list(urls)


def malicious_urls_api():
    urls =  pd.read_csv(DATASET_CSVS_PATH + 'filtered_malicious.csv')['url']
    return list(urls)


def collect_urls_into_csv(filename=urls_file_name, benign_urls_max=30000, malicious_urls_max=10000):
    print('started data gathering process')
    # shuffle all urls
    malicious_urls = malicious_urls_api()
    malicious_urls = shuffle(malicious_urls)
    benign_urls = benign_urls_api()
    benign_urls = shuffle(benign_urls)

    # slice urls as limits
    benign_urls = benign_urls[:benign_urls_max]
    malicious_urls = malicious_urls[:malicious_urls_max]

    print('Collected', len(benign_urls), 'benign urls')
    print('Collected', len(malicious_urls), 'malicious_urls')

    # make list of all urls along with label (0 / 1)
    all_urls = []
    for url in malicious_urls:
        all_urls.append([url, 1])
    for url in benign_urls:
        all_urls.append([url, 0])

    # shuffle all urls
    all_urls = shuffle(all_urls)

    # Save as csv
    print('urls saved as', filename)
    df_urls = pd.DataFrame(data=all_urls, columns=['url', 'target'])
    df_urls.to_csv(DATASET_CSVS_PATH + filename + '.csv', index=False)


if TESTING:
    collect_urls_into_csv()

