import pandas as pd
from random import shuffle
from global_variables import DEBUG, TESTING

def benign_urls_api():
    return pd.read_csv('./Dataset/all_benign.csv')['url']

def malicious_urls_api():
    return pd.read_csv('./Dataset/all_malicious.csv')['url']


def collect_urls_into_csv(filename='final_urls_dataset'):
    # serries of urls
    benign_urls = benign_urls_api()
    malicious_urls = malicious_urls_api()

    print('Collected', len(benign_urls), 'benign urls')
    print('Collected', len(malicious_urls), 'malicious_urls')

    # make list of all urls along with label (0 / 1)
    all_urls = []
    for url in malicious_urls:
        all_urls.append([url, 1])
    for url in benign_urls:
        all_urls.append([url, 0])
    
    # shuffle urls
    shuffle(all_urls)

    # Save as csv
    print('urls saved as', filename)
    df_urls = pd.DataFrame(data=all_urls, columns=['url', 'target'])
    df_urls.to_csv(r'./Dataset/' + filename + '.csv', index=False)


# if TESTING:
#     collect_urls_into_csv()
