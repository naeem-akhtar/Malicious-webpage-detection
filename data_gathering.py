import pandas as pd
from random import shuffle
from global_variables import DEBUG, TESTING, urls_file_name
 
def benign_urls_api():
    # benign1 = pd.read_csv('./Dataset/Benign_list_big_final.csv', names=['url'])['url']
    # benign2 = pd.read_csv('./Dataset/top500Domains.csv')['Root Domain']
    # return benign1.append(benign2)
    urls =  pd.read_csv('./Dataset/filtered_benign.csv')['url']
    return list(urls)


def malicious_urls_api():
    urls =  pd.read_csv('./Dataset/filtered_malicious.csv')['url']
    return list(urls)


def collect_urls_into_csv(filename=urls_file_name):
    # list of urls
    malicious_urls = malicious_urls_api()
    benign_urls = benign_urls_api()

    # take only random 5k benign urls
    shuffle(benign_urls)
    benign_urls = benign_urls[:100]
    # take only random 3k malicious urls
    shuffle(malicious_urls)
    malicious_urls = malicious_urls[:100]

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
