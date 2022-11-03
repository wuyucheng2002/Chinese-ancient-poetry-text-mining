# 合并并清洗
import pandas as pd
import os
import re


dy_dict = {'XianQin': '先秦', 'Qin': '秦', 'Han': '汉', 'WeiJin': '魏晋',
           'NanBei': '南北朝', 'Sui': '隋', 'Tang': '唐', 'Song': '宋',
           'Liao': '辽', 'Jin': '金', 'Yuan': '元', 'Ming': '明', 'Qing': '清'}

dys = ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
       'Song','Liao', 'Jin', 'Yuan', 'Ming', 'Qing']


def get_poem():
    file_list = os.listdir('D:/jisai/spider')
    poem_list = []
    for i in file_list:
        if i[0:5] == 'poem_':
            poem_list.append(i)
    return poem_list


poem_list = get_poem()
df_all = pd.DataFrame(columns=['po_id', 'au_id', 'title', 'pure-title', 'dynasty', 'big-dy', 'author',
                               'genre', 'rhyme', 'resource', 'location', 'content'], dtype=str)
for dy in dys:
    for poem in poem_list:
        if poem in ['poem_' + dy + '.csv', 'poem_' + dy + '_.csv',
                    'poem_' + dy + '0.csv', 'poem_' + dy + '1.csv']:
            df = pd.read_csv(poem, dtype=str)
            print(poem, len(df))
            if len(df) != 0:
                df = df[['po_id', 'au_id', 'title', 'dynasty', 'author',
                         'genre', 'rhyme', 'resource', 'location', 'content']]
                df['big-dy'] = dy_dict[dy]
                df = df.dropna(axis=0, subset=['po_id'])
                df_all = df_all.append(df, sort=False)

print(len(df_all))
df_all.drop_duplicates(subset='po_id', inplace=True)
length = len(df_all)
df_all.reset_index(drop=True, inplace=True)
print(length)
print(df_all)

for index, row in df_all.iterrows():
    if index % 100 == 0:
        print(index, '/', length)

    title = row['title']
    if '（' in title:
        pattern = re.compile('（[^）]*）')
        title = pattern.sub('', title)
    df_all.loc[index, 'pure-title'] = title

    if not pd.isna(row['resource']):
        if row['resource'][:3] == '出处：':
            df_all.loc[index, 'resource'] = row['resource'][3:]
    if not pd.isna(row['location']):
        if row['location'][:5] == '创作地点：':
            df_all.loc[index, 'location'] = row['location'][5:]
    # print(dict(df_all.loc[index]))

df_all.columns = ['诗词id', '作者id', '标题', '纯标题', '朝代', '朝代分类', '作者',
                  '体裁', '押韵', '出处', '创作地点', '内容']
df_all.to_csv('poem_all.csv', index=False)


