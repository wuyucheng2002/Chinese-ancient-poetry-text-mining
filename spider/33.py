# 合并诗人数据
import pandas as pd


dy_dict = {'XianQin': '先秦', 'Qin': '秦', 'Han': '汉', 'WeiJin': '魏晋',
           'NanBei': '南北朝', 'Sui': '隋', 'Tang': '唐', 'Song': '宋',
           'Liao': '辽', 'Jin': '金', 'Yuan': '元', 'Ming': '明', 'Qing': '清'}

dys = ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang',
       'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing']

df_all = pd.DataFrame(columns=['id', 'name', 'ndy', 'num', 'resource', 'intro'], dtype=str)
for dy in dys:
    name = 'D:/jisai/spider/诗人/poet_' + dy + '.csv'
    df = pd.read_csv(name, dtype=str)
    print(name, len(df))
    df['ndy'] = dy_dict[dy]
    df = df.dropna(axis=0, subset=['id'])
    df_all = df_all.append(df, sort=False)

print(len(df_all))
df_all.drop_duplicates(subset='id', inplace=True)
print(len(df_all))
print(df_all)

df_all.to_csv('poet_all.csv', index=False)