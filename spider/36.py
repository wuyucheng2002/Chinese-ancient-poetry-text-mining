# 换顺序
import pandas as pd

'''df = pd.read_csv('poet_all_address.csv')
print(list(df['address']))

df = pd.read_csv('poet_all_address.csv')
df.sort_values(by='id', ascending=True, inplace=True)
df.to_csv('poet_all_address2.csv', index=False)'''

# 写表格
au_df = []
i = 0
for dy in ['先秦', '秦', '汉', '魏晋', '南北朝', '隋', '唐', '宋',
           '辽', '金', '元', '明', '清']:
    i += 1
    au_df.append({
        'id': 100000 + i,
        'name': '无名氏',
        'ndy': dy,
        'num': '',
        'address': '',
        'resource': '',
        'intro': ''
    })
au_df = pd.DataFrame(au_df)
au_df.to_csv('wumingshi.csv', index=False)

