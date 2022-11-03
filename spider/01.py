# 爬取作者和作者的所有诗作链接
import requests
from lxml import html
from lxml import etree
import pandas as pd
import time
import re


def get_dynasty(dy):
    print(dy)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    url = 'https://www.sou-yun.cn/PoemIndex.aspx?dynasty=' + dy
    req = requests.get(url, headers=headers)
    req = req.text
    ht = html.fromstring(req)
    obj = ht.xpath('//*[@class="inline1"]/*')

    if len(obj) == 0:
        print('***error')
    else:
        au_data = []
        # po_data = []
        for i in range(0, len(obj)):
            href = obj[i].attrib['href']
            href = 'https://www.sou-yun.cn' + href
            au_id = href.split("=")[-1]

            if au_id.isdigit():
                while True:
                    try:
                        au_req = requests.get(href, headers=headers).text
                        au_ht = html.fromstring(au_req)
                        break
                    except:
                        print('***')
                        time.sleep(5)

                num = ''
                li = au_ht.xpath('//*[@class="resourceSummary"]/*')
                if len(li) != 0:
                    num = li[0].text
                    if '：' in num:
                        num = num.split("：")[1]
                        num = num[:-1]

                res = au_ht.xpath('//*[@class="poem"]//span[@class="label"]')[0]
                intro = au_ht.xpath('//*[@class="poem"]//blockquote[@class="quote1"]')[0]
                text = etree.tostring(intro, encoding='utf-8').decode('utf-8')
                text = re.sub(pattern='<.+?>', repl='', string=text)
                text = text.replace('\n', '')
                text = text.replace(' ', '')

                print(i, obj[i].text)
                au_data.append({
                    'id': au_id,
                    'name': obj[i].text,
                    'num': num,
                    'resource': res.text,
                    'intro': text
                })
                '''
                items = au_ht.xpath('//*[@class ="_poem"]')
                for item in items:
                    po_id = item.attrib['id']
                    po_id = po_id.split("_")[1]
                    po_data.append({
                        'au_id': au_id,
                        'po_id': po_id
                    })
                '''
                time.sleep(1)

        au_df = pd.DataFrame(au_data)
        au_df.to_csv("poet_" + dy + ".csv")
        # po_df = pd.DataFrame(po_data)
        # po_df.to_csv("poem_href_" + dy + ".csv")


# get_dynasty('Tang')'XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
# 'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing'


for dy in ['Qing']:
    get_dynasty(dy)
