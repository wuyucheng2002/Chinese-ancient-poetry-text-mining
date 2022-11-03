# 翻译切分
import re

with open('诗歌翻译1.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
print(len(data))

text = ''
for d in data:
    d = d.strip()
    d = d.replace(' ', '')
    # print(d)
    d1, d2 = d.split('\t')
    li1 = d1.split('。')
    li2 = d2.split('。')
    if len(li1) <= 2:
        text += d1 + '\t' + d2 + '\n'
    elif len(li1) == len(li2):
        for i in range(len(li1)-1):
            text += li1[i] + '。\t' + li2[i] + '。\n'
    else:
        text += d1 + '\t' + d2 + '\n'
        print(d1)
        print(d2)
        print()

with open('诗歌翻译2.txt', 'w', encoding='utf-8') as f:
    f.write(text)