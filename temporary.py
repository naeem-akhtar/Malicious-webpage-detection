import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options 

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/usr/bin/google-chrome'


def get_data(url, company):
    browser = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),   chrome_options=chrome_options)
    browser.get(url)
    data = browser.page_source
    browser.close()
    writer = csv.writer(file)
    
    with open('letcode_' + company + '.txt', 'w') as file:
        # file.write(str(data))
         writer.writerow([data])
    browser.quite()


if __name__ == '__main__':
    get_data(input().strip(), input().strip())
