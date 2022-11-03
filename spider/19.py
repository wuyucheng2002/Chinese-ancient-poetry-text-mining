# -*- coding: UTF-8 -*-
# 获取意象词典
import os
import pandas as pd


def get_dy():
    file_list = os.listdir('D:\@01课程资料@\计赛\spider')
    dy_list = []
    for i in file_list:
        if i[0:6] == 'image_':
            dy_list.append(i)
    return dy_list


def get_word():
    words = []
    dy_list = get_dy()
    for dy in dy_list:
        print(dy)
        df = pd.read_csv(dy)
        words += list(df['image'])
    print(len(words))
    words = list(set(words))
    print(len(words))
    # print(words)
    with open('image.txt', 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word)
            f.write('\n')

get_word()