# 把唐朝 0-12784 划分成 2000 个为一组，共 7 组
# 把明朝 0-42594 划分成 10000 个为一组，共 5 组
# 把清朝 0-53869 划分成 10000 个为一组，共 6 组
# 把Tang3 0-1999 划分成 400 个为一组，共 5 组
import pandas as pd

data = pd.read_csv('poem_href_Tang3.csv')
data = data[['au_id','po_id']]

for i in range(0, 5):
    save_data = data.iloc[i*400: (i+1)*400]
    save_data.to_csv('poem_href_Tang3' + str(i) + '.csv')
    # print(save_data)
