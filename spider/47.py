# 合并
import pandas as pd

df = pd.read_csv('poem_last3.csv', dtype=str)
ndf = pd.read_csv('poem_add.csv', dtype=str)
df = df.append(ndf, sort=False)
print(len(df))
df.drop_duplicates(subset='诗词id', inplace=True)
print(len(df))
df.to_csv('poem_last4.csv', index=False)


