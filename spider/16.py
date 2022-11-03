# 合并poem
import pandas as pd


def merge_poem(name, lis):
    save_data = pd.DataFrame()
    for li in lis:
        data = pd.read_csv(name + li + '.csv')
        print(len(data))
        save_data = save_data.append(data, sort=False)
    print('\n', len(save_data))
    print(save_data)
    save_data.to_csv(name + '.csv', index=False)


merge_poem('poem_Tang', ['0', '1', '2', '30', '31', '32', '33', '34', '4', '5', '6'])
# merge_poem('poem_Ming', ['0', '1', '2', '3', '4'])
# merge_poem('poem_Qing', ['0', '1', '2', '3', '4', '5'])




