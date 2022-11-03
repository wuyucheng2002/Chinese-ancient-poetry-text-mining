# 合并并清洗
import pandas as pd
import re

df = pd.read_csv('poem_all.csv', dtype=str)
print(len(df))

for index, row in df.iterrows():
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

    df.loc[index, '纯标题'] = title

df.to_csv('poem_all1.csv', index=False)


