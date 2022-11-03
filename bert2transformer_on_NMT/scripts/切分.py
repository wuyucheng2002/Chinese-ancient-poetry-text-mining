import pandas as pd

df = pd.read_csv('poem_last2.csv', dtype=str)
for i in range(18):
    ndf = df[1000+50000*i: 1000+50000*(i+1)]
    ndf.to_csv('poem'+ str(i) + '.csv', index=False)


