# 诗人增加地址属性
import pandas as pd

df = pd.read_csv('poet_all.csv')
df['num'] = pd.to_numeric(df['num']).astype(int)
ndf = pd.read_csv('address_author.csv')

for i, row in ndf.iterrows():
    if i % 1000 == 0:
        print(i)
    ind = df[df['id'] == row['au_id']].index.tolist()
    if len(ind) != 0:
        index = ind[0]
        if pd.isna(row['city']):
            df.loc[index, 'address'] = str(row['province']).strip()
        else:
            df.loc[index, 'address'] = str(row['province']).strip() + str(row['city']).strip()

df = df[['id', 'name', 'ndy', 'num', 'address', 'resource', 'intro']]
df.to_csv('poet_all_address.csv', index=False)
