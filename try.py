import Feature_Extraction
import numpy as np
import pandas as pd

Invalid_urls = []

df = pd.read_csv('final_dataset.csv')

print(df.columns)
i , j = 0, 0
for url in df['url']:
    input('press Any key to extract feature from next url')
    try:
        # print(i, df['target'][i], url)   # Might give error because of unidentified characters in url
        if df['target'][i+j] == 0 and i<50:
            i += 1
            print(Feature_Extraction.vector_construction(url), end='\n\n')
        elif df['target'][i+j] == 1 and j<50:
            j += 1
            print(Feature_Extraction.vector_construction(url), end='\n\n')
        else:
            break
    except:
        Invalid_urls.append(i)
        print("Cannot read this url")
    
print(df.columns)

print(Invalid_urls)
