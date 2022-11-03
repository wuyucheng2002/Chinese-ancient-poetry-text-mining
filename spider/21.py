# 抓取补充诗词和意象
import requests
from lxml import html
from lxml import etree
import pandas as pd
import re
import time


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
    df = pd.read_csv('sort_poem_' + dy + '.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    po_data = []
    for index, row in df.iterrows():
        print(index, row['name'])
        while True:
            try:
                time.sleep(1)
                url = 'https://sou-yun.cn/PoemIndex.aspx?dynasty=' + dy + '&author=' + str(row['id'])
                req = requests.get(url, headers=headers)
                req = req.text
                ht = html.fromstring(req)
                length = len(ht.xpath('//div[@class="poem"]/select/*'))
                break
            except:
                print(0, 'page-error!')

        for i in range(1, length):
            print('page ', i)
            j = 0
            while True:
                try:
                    time.sleep(1)
                    new_url = url + '&page=' + str(i)
                    req = requests.get(new_url, headers=headers)
                    req = req.text
                    ht = html.fromstring(req)
                    items = ht.xpath('//*[@class ="_poem"]')
                    po_list = []
                    for item in items:
                        po_id = item.attrib['id']
                        po_id = po_id.split("_")[1]
                        po_list.append(po_id)
                    if len(po_list) != 0:
                        break
                    else:
                        j += 1
                        print('empty-error!')
                        if j == 3:
                            break
                except:
                    print(i, 'page-error!')

            for po_id in po_list:
                po_url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + po_id
                while True:
                    try:
                        time.sleep(0.5)
                        req = requests.get(po_url, headers=headers).text
                        ht = html.fromstring(req)
                        # 标题
                        title = ht.xpath('//*[@class="poemTitle inDetail"]')[0]
                        t = etree.tostring(title, encoding='utf-8').decode('utf-8')
                        t = t.split('<span class="poemAuthor">')[0]
                        t = re.sub(pattern='<.+?>', repl='', string=t)
                        t = t.replace('\n', '')
                        t = t.replace(' ', '')
                        title = t
                        # 作者
                        author = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]')
                        author = get_text(author)
                        ndy = author.split('·')[0]
                        au = author.split('·')[1]
                        # 类别、押韵
                        indent = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="titleIndent"]')[0].text
                        genre = ''
                        rhyme = ''
                        res = ''
                        loc = ''
                        if not pd.isna(indent):
                            indent = indent.strip()
                            ind_list = indent.split()
                            for ind in ind_list:
                                if '出处：' in ind:
                                    res = ind
                                elif '创作地点：' in ind:
                                    loc = ind
                                elif '押' in ind:
                                    rhyme = ind
                                else:
                                    genre = ind
                        # 内容
                        content = ht.xpath('//*[@class="poemContent"]/*')
                        content = get_text(content)
                        break
                    except:
                        time.sleep(1)
                        print('***')

                new_po = {
                    'po_id': po_id,
                    'au_id': row['id'],
                    'title': title,
                    'dynasty': ndy,
                    'author': au,
                    'genre': genre,
                    'rhyme': rhyme,
                    'resource': res,
                    'location': loc,
                    'content': content
                }
                print(new_po)
                po_data.append(new_po)

    po_df = pd.DataFrame(po_data)
    po_df.to_csv("poem_" + dy + "_.csv", index=False)


# get_dynasty('Qin')
for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
           'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
    get_dynasty(dy)

