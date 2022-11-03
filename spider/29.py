# 生成诗词意象对应表
import pandas as pd


df = pd.DataFrame(columns=['po_id', 'im_ids'])
for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui', 'Tang']:
    ndf = pd.read_csv('poem_' + dy + '.csv')
    df = df.append(ndf[['po_id', 'im_ids']])
print(len(df))

new = []
for index, row in df.iterrows():
    im_ids = row['im_ids']
    if not pd.isna(im_ids):
        im_id_list = im_ids.split(',')
        for im_id in im_id_list:
            if im_id != '':
                new.append({
                    'po_id': row['po_id'],
                    'im_id': im_id
                })
new = pd.DataFrame(new)
print(len(new))
new.to_csv('poem_image.csv', index=False)