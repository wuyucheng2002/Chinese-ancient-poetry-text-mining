# 合并翻译
import pandas as pd
import re
import os

df = pd.DataFrame()
file_list = os.listdir('诗词翻译')
for file in file_list:
    df = df.append(pd.read_csv('诗词翻译/' + file))
print(len(df))

df.dropna(axis=0, subset=['诗id'], inplace=True)
print(len(df))

df.drop_duplicates(subset='诗id', inplace=True)
print(len(df))

df.to_csv('诗词翻译.csv', index=False)