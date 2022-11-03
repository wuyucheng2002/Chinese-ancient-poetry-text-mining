# 根据诗作的链接爬取诗作
import requests
from lxml import html
from lxml import etree
import pandas as pd
import time
import re


def get_text(xml):
    ts = ''
    for x in xml:
        t = etree.tostring(x, encoding='utf-8').decode('utf-8')
        t = re.sub(pattern='<.+?>', repl='', string=t)
        t = t.replace('\n', '')
        t = t.replace(' ', '')
        ts += t
    return ts


def get_dynasty(dy):
    print(dy)
    df = pd.read_csv('poem_href_' + dy + '.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    po_data = []
    for index, row in df.iterrows():
        print(index)
        while True:
            try:
                url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + str(row['po_id'])
                req = requests.get(url, headers=headers)
                req = req.text
                ht = html.fromstring(req)
                # 标题
                title = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]/preceding-sibling::*')
                title = get_text(title)
                # 作者
                author = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]')
                author = get_text(author)
                # 类别、押韵
                indent = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="titleIndent"]')[0].text
                # 内容
                content = ht.xpath('//*[@class="poemContent"]/*')
                content = get_text(content)
                po = {
                    'po_id': row['po_id'],
                    'au_id': row['au_id'],
                    'title': title,
                    'author': author,
                    'indent': indent,
                    'content': content
                }
                po_data.append(po)
                time.sleep(1)
                break
            except:
                print("error!")
                time.sleep(3)

    po_df = pd.DataFrame(po_data)
    po_df.to_csv("poem_" + dy + ".csv")


# get_dynasty('Qin')
# 'Ming0', 'Ming1', 'Ming2', 'Ming3','Ming4','Qing0', 'Qing1', 'Qing2', 'Qing3',
for dy in ['Qing4', 'Qing5']:
    get_dynasty(dy)
