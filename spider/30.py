# 统计地址
import pandas as pd
import numpy as np


df = pd.read_csv('address_author.csv')

dy_dict = {
    '先秦': 'XianQin',
    '秦': 'Qin',
    '汉': 'Han',
    '魏晋': 'WeiJin',
    '南北朝': 'NanBei',
    '隋': 'Sui',
    '唐': 'Tang',
    '宋': 'Song',
    '辽': 'Liao',
    '金': 'Jin',
    '元': 'Yuan',
    '明': 'Ming',
    '清': 'Qing'
}

pr_list = list(set(df['province']))
# print(pr_list)
# print(len(pr_list))  # 34
au_df = pd.DataFrame(columns=pr_list, index=dy_dict.keys(), data=np.zeros([13,34]).astype(int))
po_df = pd.DataFrame(columns=pr_list, index=dy_dict.keys(), data=np.zeros([13,34]).astype(int))

for index, row in df.iterrows():
    if index % 100 == 0:
        print(index)
    p = row['province']
    d = row['dynasty']
    if d not in ['近现代', '当代']:
        au_df.loc[d, p] += 1
        dy = dy_dict[d]
        au_id = row['au_id']
        new_df = pd.read_csv('poet_' + dy + '.csv')
        a = new_df[new_df['id'] == au_id].index.tolist()
        if len(a) != 0:
            a = a[0]
            num = new_df.loc[a, 'num']
            po_df.loc[d, p] += num
        else:
            print('*', au_id)

print(au_df)
print(po_df)
au_df.to_csv('address_dy_author.csv')
po_df.to_csv('address_dy_poem.csv')
