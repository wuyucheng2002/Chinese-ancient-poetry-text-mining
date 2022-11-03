# 爬取古诗文网诗词和翻译
import re
import gc
import requests
import random
import time
import numpy as np
import pandas as pd
requests.packages.urllib3.disable_warnings()

proxy_list = [{'http': '118.113.246.131:9999'},
              {'http': '36.249.109.18:9999'},
              {'http': '114.104.142.65:9999'},
              {'http': '113.128.31.217:9999'},
              {'http': '171.12.112.155:9999'},
              {'http': '1.197.16.218:9999'},
              {'http': '182.34.36.100:9999'},
              {'http': '36.249.119.34:9999'},
              {'http': '175.43.59.4:9999'},
              {'http': '113.124.87.65:9999'},
              {'http': '125.108.81.211:9999'},
              {'http': '175.42.68.194:9999'},
              {'http': '183.166.97.166:9999'},
              {'http': '180.118.128.112:9000'},
              {'http': '60.13.42.151:9999'},
              {'http': '182.149.83.194:9999'},
              {'http': '60.205.132.71:80'},
              {'http': '120.79.64.147:8118'},
              {'http': '121.232.194.144:9000'},
              {'http': '171.35.160.55:9999'},
              {'http': '36.248.129.82:9999'},
              {'http': '171.15.48.137:9999'},
              {'http': '163.204.245.210:9000'},
              {'http': '117.88.5.116:3000'},
              {'http': '144.123.71.3:9999'},
              {'http': '125.108.81.211:9999'},
              {'http': '120.234.138.102:53779'},
              {'http': '175.42.68.194:9999'},
              {'http': '120.83.105.247:9999'},
              {'http': '112.111.217.56:9999'}]


def get_json(url):
    while True:
        # proxy = random.choice(proxy_list)
        try:
            response = requests.get(url, verify=False)  # , proxies=proxy
            if response.status_code == 200:
                return response.json()
            else:
                print(str(response.status_code), '等待1秒..')  # , proxy
                time.sleep(1)
        except:
            print('等待1秒..')  # , proxy
            time.sleep(1)


def get_Yijson(url):
    while True:
        # proxy = random.choice(proxy_list)
        try:
            response = requests.get(url, verify=False)  # , proxies=proxy
            if response.status_code == 200:
                return response.json()
            else:
                return ''
        except:
            print('等待1秒..')  # , proxy
            time.sleep(1)


def clear(cont):
    cont = cont.replace('\u3000', '')
    cont = cont.replace('\n', '')
    cont = cont.replace('\r', '')
    cont = cont.replace('\t', '')
    resub1 = r'译注内容由匿名网友上传，原作者已无法考证。' \
             r'古诗文网免费发布仅供学习参考，其观点不代表古诗文网立场。邮箱：service@gushiwen.org'
    resub2 = r'赏析内容由匿名网友上传，原作者已无法考证。' \
             r'古诗文网免费发布仅供学习参考，其观点不代表古诗文网立场。邮箱：service@gushiwen.org'
    cont = cont.replace(resub1, '')
    cont = cont.replace(resub2, '')
    return cont


def get_author():
    authorList = []
    cs = ['先秦', '两汉', '魏晋', '南北朝', '隋代', '唐代',
          '五代', '宋代', '金朝', '元代', '明代', '清代']
    for c in cs:
        print(c)
        json = get_json('https://app.gushiwen.cn:443/api/author/Default10.aspx?c=' + c +
                        '&page=1&token=gswapi')
        pages = json.get('sumPage')
        for i in range(1, pages + 1):
            print(i, '/', pages)
            json = get_json('https://app.gushiwen.cn:443/api/author/Default10.aspx?c=' + c +
                            '&page=' + str(i) + '&token=gswapi')
            gs = json.get('authors')
            for g in gs:
                nameStr = g.get('nameStr')
                cont = g.get('cont')
                idnew = g.get('idnew')
                authorList.append([nameStr, cont, idnew])
    return authorList


def get_shi(authorName):
    shiciList = []
    url = 'https://app.gushiwen.cn:443/api/shiwen/Default11.aspx?token=gswapi&page=0&astr=' + str(authorName)
    json = get_json(url)
    if json != '':
        sumPage = json.get('sumPage')
        sumCount = json.get('sumCount')
        print(authorName, sumPage, sumCount)
        for page in range(1, sumPage + 1):
            url = 'https://app.gushiwen.cn:443/api/shiwen/Default11.aspx?token=gswapi&page=' + \
                  str(page) + '&astr=' + str(authorName)
            pageJson = get_json(url)
            # time.sleep(0.1)
            if pageJson == '':
                print('没抓取到啊')
            else:
                for g in pageJson.get('gushiwens'):
                    idnew = g['idnew']
                    shiciList.append(idnew)
    else:
        print('else')
    print('shiciList', len(shiciList))
    return shiciList


def get_content(idnews):
    url = 'https://app.gushiwen.cn:443/api/shiwen/shiwenv11.aspx?id=' + str(idnews) + '&token=gswapi'
    json = get_json(url)
    # time.sleep(0.05)
    nameStr = json.get('tb_gushiwen').get('nameStr')  # 诗的名字
    author = json.get('tb_gushiwen').get('author')   # 作者
    chaodai = json.get('tb_gushiwen').get('chaodai')  # 朝代
    cont = json.get('tb_gushiwen').get('cont')  # 诗词内容
    cont = clear(cont)
    tag = json.get('tb_gushiwen').get('tag')  # "高中古诗|乐府|唐诗三百首|抒情|哲理|忧愤"
    fanyiList = json.get('tb_fanyis').get('fanyis')
    fanyicont = ''  # 翻译内容
    fanyicankao = ''  # 翻译参考
    if len(fanyiList) > 0:
        fanyicont = fanyiList[0].get('cont')
        fanyicont = clear(fanyicont)
        fanyicankao = fanyiList[0].get('cankao')
        fanyicankao = clear(fanyicankao)
    '''shangxiList= []  # 赏析列表
    shangxiDict = json.get('tb_shangxis').get('shangxis')
    if len(shangxiDict) > 0:
        for shangxi in shangxiDict:
            shangxidic = {}
            shangxidic['nameStr'] = shangxi['nameStr']
            shangxidic['cont'] = re.sub(r'\u3000', '', shangxi['cont'])
            shangxidic['cankao'] = shangxi['cankao']
            shangxiList.append(shangxidic)
    # 诗人介绍
    # authorjieshao = json.get('tb_author').get('cont')'''
    return str(nameStr), str(author), str(chaodai), str(cont), str(tag), str(fanyicont), str(fanyicankao)


def get_yizhushang(idnews):
    try:
        yi = get_Yijson('https://app.gushiwen.cn:443/api/shiwen/ajaxshiwencont11.aspx?token=gswapi&idnew=' +
                        str(idnews) + '&value=yi')
        yicont = clear(yi.get('cont'))
        yicankao = clear(yi.get('cankao'))
    except:
        yicont = ''
        yicankao = ''
    try:
        zhu = get_Yijson('https://app.gushiwen.cn:443/api/shiwen/ajaxshiwencont11.aspx?token=gswapi&idnew=' +
                         str(idnews) + '&value=zhu')
        zhucont = clear(zhu.get('cont'))
        zhucankao = clear(zhu.get('cankao'))
    except:
        zhucont = ''
        zhucankao = ''
    try:
        shang = get_Yijson('https://app.gushiwen.cn:443/api/shiwen/ajaxshiwencont11.aspx?token=gswapi&idnew=' +
                           str(idnews) + '&value=shang')
        shangcont = clear(shang.get('cont'))
        shangcankao = clear(shang.get('cankao'))
    except:
        shangcont = ''
        shangcankao = ''
    return str(yicont), str(yicankao), str(zhucont), str(zhucankao), str(shangcont), str(shangcankao)


def get_authorziliaos(idnew):
    url = 'https://app.gushiwen.cn/api/author/author10.aspx?id='+ str(idnew) + '&token=gswapi'
    json = get_json(url)
    ziliaoList= []  # 赏析列表
    ziliaosDict = json.get('tb_ziliaos').get('ziliaos')
    if len(ziliaosDict) > 0:
        for ziliao in ziliaosDict:
            ziliaodic = {}
            ziliaodic['nameStr'] = ziliao['nameStr']
            ziliaodic['cont'] = re.sub(r'\u3000', '', ziliao['cont'])
            ziliaodic['cankao'] = ziliao['cankao']
            ziliaoList.append(ziliaodic)
        return str(ziliaoList)


def getList():
    list = []
    name_list = ['%E8%AF%97']  # , '%E8%AF%8D', '%E6%9B%B2', '%E6%96%87%E8%A8%80%E6%96%87'
    for name in name_list:
        for i in range(1, 11):
            json = get_json('https://app.gushiwen.cn/api/shiwen/Default11.aspx?xstr=' + name +
                            '&page=' + str(i) + '&token=gswapi')
            gushiwens = json.get('gushiwens')
            for r in range(10):
                idnew = gushiwens[r]['idnew']
                list.append(idnew)
    return list


if __name__ == '__main__':
    au_df = pd.read_csv('作者信息.csv')
    data = []
    n = 112000
    for i, row in au_df.iterrows():
        if i < 1786:
            continue
        shi_li = get_shi(row['姓名'])
        for shi in shi_li:
            n += 1
            if n % 1000 == 0:
                # data = np.array(data)
                df = pd.DataFrame(data)
                df.columns = ['诗id', '名称', '作者', '朝代', '内容', '标签', '翻译', '翻译参考',
                              '译', '译参考', '注', '注参考', '赏', '赏参考']
                df.to_csv('诗词翻译' + str(n) + '.csv', index=False)
                print('已保存', n, '首！')
                del df, data, gg
                gc.collect()
                data = []
            gg = (shi, ) + get_content(shi) + get_yizhushang(shi)
            data.append(gg)
            if n % 100 == 1:
                print('【', n, '】', gg[:6])
    df = pd.DataFrame(data)
    df.columns = ['诗id', '名称', '作者', '朝代', '内容', '标签', '翻译', '翻译参考',
                  '译', '译参考', '注', '注参考', '赏', '赏参考']
    df.to_csv('诗词翻译' + str(n) + '.csv', index=False)
    print('已保存', n, '首！')

