# 统计所有诗人
import pandas as pd


df = pd.DataFrame(columns=['id', 'name', 'num'])
for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
           'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']:
    ndf = pd.read_csv('sort_poem_' + dy + '.csv')
    df = df.append(ndf)
print(len(df))
df.drop_duplicates(inplace=True)
print(len(df))
df.sort_values(by='num', ascending=False, inplace=True)
df = df.iloc[0:15]
print(df)
df.to_csv('sort_poem_all.csv', index=False)