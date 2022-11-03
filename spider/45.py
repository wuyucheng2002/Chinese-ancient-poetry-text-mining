# 爬纳兰性德、李清照
import pandas as pd
import requests
from lxml import html
from lxml import etree
import time
import re

# https://sou-yun.cn/PoemIndex.aspx?dynasty=Song&author=27794
# https://sou-yun.cn/PoemIndex.aspx?dynasty=Qing&author=68611


def get_text(xml):
    ts = ''
    for x in xml:
        t = etree.tostring(x, encoding='utf-8').decode('utf-8')
        t = re.sub(pattern='<.+?>', repl='', string=t)
        t = t.replace('\n', '')
        t = t.replace(' ', '')
        ts += t
    return ts


def get_poem(id, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    po_data = []

    while True:
        try:
            time.sleep(1)
            req = requests.get(url, headers=headers).text
            ht = html.fromstring(req)
            length2 = len(ht.xpath('//div[@class="poem"]/select/*'))
            break
        except:
            print('page-error!')

    for i in range(0, length2):
        print('page:', i+1, '/', length2)
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
                    print('empty-error!')

            except:
                print(i, 'page-error!')

        for po_id in po_list:
            po_url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + po_id
            j = 0
            while True:
                try:
                    time.sleep(1)
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
                    # 保存
                    new_po = {
                       'po_id': po_id,
                       'au_id': id,
                       'title': title,
                       'dynasty': ndy,
                       'author': au,
                       'genre': genre,
                       'rhyme': rhyme,
                       'resource': res,
                       'location': loc,
                       'content': content
                    }
                    print(new_po['title'], new_po['author'])
                    po_data.append(new_po)
                    break

                except:
                    print("***", j)
                    time.sleep(1)
                    j += 1
    po_df = pd.DataFrame(po_data)
    po_df.to_csv(id + '.csv')


get_poem('27794', 'https://sou-yun.cn/PoemIndex.aspx?dynasty=Song&author=27794')
get_poem('68611', 'https://sou-yun.cn/PoemIndex.aspx?dynasty=Qing&author=68611')
