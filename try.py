# from prediction import predict
import os
import re
import csv
import whois
import json
import datetime
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 
from Feature_Extraction import host_based_features, content_based_features
from global_variables import DEBUG

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/usr/bin/google-chrome'
browser = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options)


def dateConverter(obj):
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


def website_information(url):
    who, data = '', ''
    try:
        if requests.head(url).status_code == 200:
            # whois
            try:
                who = whois.whois(url)
            except KeyboardInterrupt:
                raise
            except Exception as error:
                print('No whois information')
                print(error)

            # website source code
            try:
                # browser.get(url)
                # data = browser.page_source
                # browser.close()
                data = requests.get(url)
            except KeyboardInterrupt:
                raise
            except Exception as error:
                print('Cannot reach website')
                print(error)
            
            who, data = json.dumps(who, default=dateConverter), str(data)
    except KeyboardInterrupt:
        raise
    except Exception as error:
        print('url does not exist')
        print(error)

    # print(type(who).encode('utf-8'), type(data).encode('utf-8'))
    return [who, data]


def add_new_data_to_csv(index):
    urls = list(pd.read_csv('./Dataset/filtered_malicious.csv')['url'])

    with open('./Dataset/urls_scrapping.csv', 'w') as file:
        # header = ['index', 'url', 'whois', 'website_data', 'label']
        writer = csv.writer(file)
        # writer.writeheader()
        for i in range(index, len(urls)):
            # print(urls)
            writer.writerow([i, urls[i]] + website_information(urls[i]) + [1])
            if i%10 == 0:
                print('completed', i)


def add_more_websites_data():
    # find next url index which has to be done
    input_file = open('./Dataset/urls_scrapping.csv',"r+")
    reader_file = csv.reader(input_file)
    next_index = len(list(reader_file))

    print('Starting from index :', next_index)
    add_new_data_to_csv(next_index)


def extract_features():
    df = pd.read_csv('./Dataset/urls_scrapping.csv', names=['index', 'url', 'whois', 'website_data', 'label'])
    for i in range(len(df)):
        url = df['url'][i]
        # null = ''
        print(df['whois'][i])
        print()
        # break
        without_protocol = re.sub(r'^www.', '', re.sub(r'^http(s*)://', '', url))
        print(url)
        print('Host :', host_based_features(url, without_protocol, json.loads(df['whois'][i])))
        print('Content :', content_based_features(url, without_protocol, df['website_data'][i]))


if __name__ == '__main__':
    try:
        # print(content_based_features(input()))
        # driver.get('https://www.google.com')
        # print(driver.page_source)
        # print(website_information(input().strip()))
        add_more_websites_data()
        # extract_features()
        # print(website_information('http://www.google.com'))
    except Exception as error:
        print("program stopped.", error)
    browser.quit()

# def check_prediction():
#     for _ in range(int(input('Enter number of urls: '))):
#         try:
#             print('Malicious :(' if predict(input()) else 'Safe :)')
#         except:
#             print("Cannot check this url :(")
#             break


# # response time consideration
# def req_time(url):
#     try:
#         response = requests.get(url, timeout=3)
#         return round((response.elapsed.total_seconds()*1000))
#     except Exception as error:
#         # print(error)
#         return 3000

# def test_urls():
#     urls = pd.read_csv('./Dataset/final_urls_dataset.csv')
#     df = pd.DataFrame(columns=['response_time', 'label'])

#     for i in range(len(urls)):
#         url = urls.iloc[i]['url']
#         label = urls.iloc[i]['target']

#         try:
#             requests.head(url)
#             time = req_time(url)
#             df.loc[i] = [time, label]
#             print(time, i, label, url[:20], sep=' | ')
#         except:
#             pass
#         if  i >= 100:
#             break
#     # df.to_csv('./Dataset/response_time.csv', index=False)

