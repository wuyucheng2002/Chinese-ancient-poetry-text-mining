import pandas as pd


df_all = pd.DataFrame()
li = ['1000', ] + [str(i) for i in range(18)]
for l in li:
    file = 'poems/poem' + l + '_.csv'
    df = pd.read_csv(file, dtype=str)
    print(file, len(df))
    df_all = df_all.append(df, sort=False)

print(len(df_all))

df_all.to_csv('poem_last3.csv', index=False)