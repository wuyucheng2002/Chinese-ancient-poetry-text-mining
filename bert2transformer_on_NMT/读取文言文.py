'''import os

files = os.listdir('bitext')
print(files)
text = ''
for file in files:
    with open('bitext/' + file, 'r', encoding='utf-8') as f:
        data = f.readlines()
        i = 0
        print(len(data))
        while i < len(data):
            src = data[i].strip()[3:]
            tgt = data[i + 1].strip()[4:]
            text += src + '\t' + tgt + '\n'
            i += 3

with open('文言文.txt', 'w', encoding='utf-8') as f:
    f.write(text)'''

'''text = ''
with open('新唐书', 'r', encoding='utf-8') as f:
    data = f.readlines()
    i = 0
    print(len(data))
    while i < len(data):
        src = data[i].strip()[3:]
        tgt = data[i + 1].strip()[4:]
        text += src + '\t' + tgt + '\n'
        i += 3

with open('新唐书.txt', 'w', encoding='utf-8') as f:
    f.write(text)'''

import re

with open('诗歌翻译.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
print(len(data))

text = ''
for d in data:
    d = d.strip()
    d = d.replace('&nbsp;', '')
    d = d.replace(' ', '')
    d = re.sub(pattern='(.+?)', repl='', string=d)
    d1, d2 = d.split('\t')
    # if '。' in d1 and '。' in d2:
    li1 = d1.split('。')
    li2 = d2.split('。')
    if len(li1) == len(li2) and len(li1) > 2:
        for i in range(len(li1)-1):
            text += li1[i] + '\t' + li2[i] + '\n'
    else:
        print(d1)
        print(d2)
        print()
        text += d1 + '\t' + d2 + '\n'

