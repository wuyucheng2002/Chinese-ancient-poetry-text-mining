# 合并多个csv，处理image
import pandas as pd


def merge_image(name, lis):
    save_data = pd.DataFrame(columns=['id', 'image', 'pronunciation', 'resource', 'explain'])

    for li in lis:
        data = pd.read_csv(name + li + '.csv')
        data = data[['id', 'image', 'explain']]
        data = data.dropna(axis=0, how='any')
        print(len(data))
        save_data = save_data.append(data, sort=False)
    print('\n', len(save_data))

    save_data.drop_duplicates(subset=['id'], inplace=True)
    save_data.index = range(len(save_data))
    print('\n', len(save_data))

    for index, row in save_data.iterrows():
        if index % 1000 == 0:
            print(index)

        # print(row)
        image = row['image']
        explain = row['explain']

        if '分类：' in explain:
            behind = explain.split('分类：')[-1]
            explain = explain[len(image): - len('分类：' + behind)]
        else:
            explain = explain[len(image): -1]
        save_data.loc[index, 'explain'] = explain.replace(' ', '')

        if '拼音：' in image:
            pron = image.split('拼音：')[1]
            image = image[: - len('拼音：' + pron)]
        else:
            pron = ''

        res = image.split("》")[0] + '》'
        image = image[len(res + '：'):]
        image = image.replace(' ', '')
        image = image.strip()

        if '（' in image:
            image = image.split('（')[0]

        save_data.loc[index, 'image'] = image
        save_data.loc[index, 'pronunciation'] = pron
        save_data.loc[index, 'resource'] = res
        # print(save_data.loc[index])

    print('\n', len(save_data))
    # print(save_data)
    save_data.to_csv(name + '_.csv', index=False)


merge_image('image_Tang', ['0', '1', '2', '30', '31', '32', '33', '34', '4', '5', '6'])
for dy in ['XianQin', 'Qin', 'Han', 'WeiJin', 'NanBei', 'Sui']:
    merge_image('image_' + dy, [''])
