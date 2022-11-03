# 获取翻译
import pandas as pd
import re
'''
df = pd.read_csv('诗词翻译.csv')
df.dropna(axis=0, subset=['译'], inplace=True)
print(len(df))
li = list(df['译'])
with open('诗歌翻译.txt', 'w', encoding='utf-8') as f:
    f.writelines([l + '\n' for l in li])
'''
''''''
with open('诗歌翻译.txt', 'r', encoding='utf-8') as f:
    li = f.readlines()

text = ''
k = 0
for l in li:
    l.strip()
    l = l.replace('&nbsp;', '')
    l = re.sub(pattern='（[^（）]*）', repl='', string=l)
    l = re.sub(pattern='\([^\(\)]*\)', repl='', string=l)
    if '<span style="color:#af9100;">' in l:
        k += 1
        str = re.split('<br /><span style=""color:#af9100;"">|</span></p>|</span><br /></p>|'
                       '<br /></span>|<br /><span style="color:#af9100;">|<span style="color:#af9100;">|'
                       '<span style=""color:#af9100;"">', l)
        str = [re.sub(pattern='<[^<>]*>', repl='', string=s) for s in str]
        str = [s.strip() for s in str if s.strip() != '']
        if len(str) % 2 == 1:
            print(l)
            print(str)
            print()
        for i in range(len(str)//2):
            text += str[2*i] + '\t' + str[2*i+1] + '\n'
print(k)
with open('诗歌翻译1.txt', 'w', encoding='utf-8') as f:
    f.write(text)

