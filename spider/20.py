# 补救poet
import requests
from lxml import html
import pandas as pd
import time

def clear_poet(dy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    print(dy)
    data = pd.read_csv('poet_' + dy + '.csv')
    data = data[['id', 'name', 'num', 'resource', 'intro']]
    for index, row in data.iterrows():
        num = row['num']
        # if num == '相关诗词':
        if pd.isna(num):
            print(row)
            href = 'https://sou-yun.cn/PoemIndex.aspx?dynasty=' + dy + '&author=' + str(row['id'])
            while True:
                try:
                    time.sleep(1)
                    au_req = requests.get(href, headers=headers).text
                    au_ht = html.fromstring(au_req)
                    break
                except:
                    print('***')
                    time.sleep(5)

            items = au_ht.xpath('//*[@class ="_poem"]')
            print(len(items))
            data.loc[index, 'num'] = len(items)
    data.to_csv('poet_' + dy + '.csv', index=False)


# get_dynasty('Tang')'XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
# 'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing'

for dy in ['Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
    clear_poet(dy)
