# 统计诗人
import pandas as pd


dy_dict = {'XianQin': '先秦', 'Qin': '秦', 'Han': '汉', 'WeiJin': '魏晋',
           'NanBei': '南北朝', 'Sui': '隋', 'Tang': '唐', 'Song': '宋',
           'Liao': '辽', 'Jin': '金', 'Yuan': '元', 'Ming': '明', 'Qing': '清'}

dys = ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
       'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']

df = pd.read_csv('poet_all.csv', usecols=['id', 'name', 'ndy', 'num'],
                 dtype={'id': str, 'name': str, 'ndy': str, 'num': int})
df.sort_values(by='num', ascending=False, inplace=True)
ndf = df.iloc[0:10]
ndf.to_csv('sort_poem_all.csv', index=False)

for dy in dys:
    print(dy)
    ndf = df[df['ndy'] == dy_dict[dy]]
    length = min(len(ndf), 10)
    ndf = ndf.iloc[0:length]
    ndf.to_csv('sort_poem_' + dy + '.csv', index=False)





