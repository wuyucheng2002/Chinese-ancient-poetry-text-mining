# 合并并清洗
import pandas as pd
import re

df_all = pd.DataFrame(columns=['po_id', 'au_id', 'title', 'pure-title', 'dynasty', 'big-dy', 'author',
                               'genre', 'rhyme', 'resource', 'location', 'content'], dtype=str)

df = pd.read_csv('27794.csv', dtype=str)
print(len(df))
df = df[['po_id', 'au_id', 'title', 'dynasty', 'author',
         'genre', 'rhyme', 'resource', 'location', 'content']]
df['big-dy'] = '宋'
df = df.dropna(axis=0, subset=['po_id'])
df_all = df_all.append(df, sort=False)

df = pd.read_csv('68611.csv', dtype=str)
print(len(df))
if len(df) != 0:
    df = df[['po_id', 'au_id', 'title', 'dynasty', 'author',
             'genre', 'rhyme', 'resource', 'location', 'content']]
    df['big-dy'] = '清'
    df = df.dropna(axis=0, subset=['po_id'])
    df_all = df_all.append(df, sort=False)

print(len(df_all))
df_all.drop_duplicates(subset='po_id', inplace=True)
length = len(df_all)
df_all.reset_index(drop=True, inplace=True)
print(length)
print(df_all)

for index, row in df_all.iterrows():
    # if index % 1000 == 0:
    #     print(index, '/', length)

    title = row['title']
    if '（' in title:
        pattern = re.compile('（[^（）]*）')
        for i in range(10):
            if '（' in title:
                title = pattern.sub('', title)
            else:
                break
        if '（' in title or '）' in title:
            print(index, title)

    if '(' in title:
        pattern = re.compile('\([^\(\)]*\)')
        for i in range(10):
            if '(' in title:
                title = pattern.sub('', title)
            else:
                break
        if '(' in title or ')' in title:
            print(index, title)

    df_all.loc[index, 'pure-title'] = title

    if not pd.isna(row['resource']):
        if row['resource'][:3] == '出处：':
            df_all.loc[index, 'resource'] = row['resource'][3:]
    if not pd.isna(row['location']):
        if row['location'][:5] == '创作地点：':
            df_all.loc[index, 'location'] = row['location'][5:]

df_all.columns = ['诗词id', '作者id', '标题', '纯标题', '朝代', '朝代分类', '作者',
                  '体裁', '押韵', '出处', '创作地点', '内容']

for index, row in df_all.iterrows():
    # if index % 1000 == 0:
    #     print(index, '/', length)

    title = row['标题']
    if '（' in title:
        pattern = re.compile('（[^（）]*）')
        for i in range(10):
            if '（' in title:
                title = pattern.sub('', title)
            else:
                break
        if '（' in title or '）' in title:
            print(index, title)

    if '(' in title:
        pattern = re.compile('\([^\(\)]*\)')
        for i in range(10):
            if '(' in title:
                title = pattern.sub('', title)
            else:
                break
        if '(' in title or ')' in title:
            print(index, title)

    df_all.loc[index, '纯标题'] = title

    title = row['内容']
    if '（' in title:
        pattern = re.compile('（[^（）]*）')
        for i in range(10):
            if '（' in title:
                title = pattern.sub('', title)
            else:
                break
        if '（' in title or '）' in title:
            print(index, title)

    if '(' in title:
        pattern = re.compile('\([^\(\)]*\)')
        for i in range(10):
            if '(' in title:
                title = pattern.sub('', title)
            else:
                break
        if '(' in title or ')' in title:
            print(index, title)
    df_all.loc[index, '纯内容'] = title


df_all.to_csv('poem_add.csv', index=False)


