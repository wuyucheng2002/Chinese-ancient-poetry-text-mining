# 补救poem
import re
import requests
import time
import pandas as pd
from lxml import html
from lxml import etree


def clear_poem(name):
    print(name)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    data = pd.read_csv('poem_' + name + '.csv')
    # print(len(data))
    for index, row in data.iterrows():
        time.sleep(1)
        url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + str(row['po_id'])
        while True:
            try:
                req = requests.get(url, headers=headers).text
                ht = html.fromstring(req)
                break
            except:
                print('***')
                time.sleep(5)
        # 标题
        title = ht.xpath('//*[@class="poemTitle inDetail"]')[0]
        t = etree.tostring(title, encoding='utf-8').decode('utf-8')
        t = t.split('<span class="poemAuthor">')[0]
        t = re.sub(pattern='<.+?>', repl='', string=t)
        t = t.replace('\n', '')
        t = t.replace(' ', '')
        print(index, row['title'], t)
        data.loc[index, 'title'] = t

    data.to_csv('poem_' + name + '.csv', index=False)


for dy in ['Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
    clear_poem(dy)
