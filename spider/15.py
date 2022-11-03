# 补救poem，处理poem
import os
import requests
import time
import pandas as pd
from lxml import html


def get_poem():
    file_list = os.listdir('D:\@01课程资料@\计赛\spider')
    poem_list = []
    for i in file_list:
        if i[0:5] == 'poem_':
            poem_list.append(i)
    return poem_list


def clear_poem(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    new_data = []
    print(name)
    data = pd.read_csv(name)
    if 'im_ids' in data.columns:
        tag = True
    else:
        tag = False

    # print(len(data))
    for index, row in data.iterrows():
        title = row['title']
        if pd.isna(title):
            print(index)
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
            title = ht.xpath('//*[@class="poemTitle inDetail"]')[0]
            title = title.text

        dy = row['author'].split('·')[0]
        au = row['author'].split('·')[1]

        genre = ''
        rhyme = ''
        res = ''

        if not pd.isna(row['indent']):
            indent = row['indent'].strip()
            ind_list = indent.split()
            for ind in ind_list:
                if '出处：' in ind:
                    res = ind
                elif '押' in ind:
                    rhyme = ind
                else:
                    genre = ind

        if tag:
            new_data.append({
                'po_id': row['po_id'],
                'au_id': row['au_id'],
                'title': title,
                'dynasty': dy,
                'author': au,
                'genre': genre,
                'rhyme': rhyme,
                'resource': res,
                'content': row['content'],
                'im_ids': row['im_ids']
            })
        else:
            new_data.append({
                'po_id': row['po_id'],
                'au_id': row['au_id'],
                'title': title,
                'dynasty': dy,
                'author': au,
                'genre': genre,
                'rhyme': rhyme,
                'resource': res,
                'content': row['content']
            })

    df = pd.DataFrame(new_data)
    df.to_csv(name, index=False)


poem_list = get_poem()
for poem in poem_list:
    clear_poem(poem)
