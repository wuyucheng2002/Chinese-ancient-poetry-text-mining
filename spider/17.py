# 统计数据
import pandas as pd
import jieba
from collections import Counter
import re
import time
jieba.load_userdict("image.txt")


def get_sum(dy):
    print(dy)
    au_df = pd.read_csv('poet_' + dy + '.csv')
    au_sum = len(au_df)
    # au_df.loc[pd.isna(au_df['num']), 'num'] = 0
    au_df['num'] = au_df['num'].astype(int)
    po_sum = sum(au_df['num'])
    print(po_sum, au_sum)
    au_df.sort_values(by='num', ascending=False, inplace=True)
    length = min(15, len(au_df))
    new_df = au_df.iloc[0:length, 0:3]
    # print(new_df)
    new_df.to_csv('sort_poem_' + dy + '.csv', index=False)
    return po_sum, au_sum


def get_word(dy):
    print(dy)
    po_df = pd.read_csv('poem_' + dy + '.csv')
    texts = list(po_df['content'])
    c = Counter()
    for text in texts:
        pattern = re.compile('（[^）]*）')
        t = pattern.sub('', text)
        word_list = [w for w in jieba.cut(t, cut_all=False) if w not in punc]
        for word in word_list:
            c[word] += 1
        images = []
        for (k, v) in c.most_common(300):
            images.append({
                'image': k,
                'num': v
            })
        im_df = pd.DataFrame(images)
        im_df.to_csv('sort_image_' + dy + '.csv', index=False)


def get_all1():
    dd = []
    for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
               'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
        po, au = get_sum(dy)
        dd.append({
            'dyansty': dy,
            'po_num': po,
            'au_num': au
        })
        df = pd.DataFrame(dd)
        df.to_csv('sort_all.csv', index=False)


def get_all2():
    for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
               'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
        time.sleep(3)
        get_word(dy)


punc = '，。、【 】「」 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
# get_all1()
get_all2()