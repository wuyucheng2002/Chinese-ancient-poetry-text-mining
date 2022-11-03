# 合并并清洗
import pandas as pd
import re


dy_dict = {'XianQin': '先秦', 'Qin': '秦', 'Han': '汉', 'WeiJin': '魏晋',
           'NanBei': '南北朝', 'Sui': '隋', 'Tang': '唐', 'Song': '宋',
           'Liao': '辽', 'Jin': '金', 'Yuan': '元', 'Ming': '明', 'Qing': '清'}

dys = ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
       'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']

df_all = pd.DataFrame(columns=['po_id', 'au_id', 'title', 'pure-title', 'dynasty', 'big-dy', 'author',
                               'genre', 'rhyme', 'resource', 'location', 'content'], dtype=str)

for dy in dys:
    poem = 'poem_' + dy + '1.csv'
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
df_all.to_csv('poem_all2.csv', index=False)


