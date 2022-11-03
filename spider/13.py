# 爬取地址
import requests
from lxml import html
import pandas as pd
import time
from lxml import etree

def get_address():
    str1 = '<p><span class="squareLabel1">'
    str2 = '<p><span class="inlineComment2">'
    str3 = '</span></p>'
    str4 = '" class="expand">'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    url = 'https://sou-yun.cn/IndexByMap.aspx'

    pr_data = []
    cc_data = []
    ci_data = []
    req = requests.get(url, headers=headers)
    req = req.text
    ht = html.fromstring(req)
    lis = ht.xpath('//*[@class="ProvinceBlock"][1]//a')
    for li in lis:
        href = li.attrib['href']
        province = li.text
        print(province)
        num = li.xpath('span')[0].text
        pr_data.append({
            'province': province,
            'num': num
        })
        # 城市
        time.sleep(1)
        ci_url = 'https://sou-yun.cn' + href
        ci_req = requests.get(ci_url, headers=headers).text
        ci_ht = html.fromstring(ci_req)
        cc = ci_ht.xpath('//div[@style="margin: 0.5em;"]/p/a')
        for c in cc:
            city = c.text
            num = c.xpath('span')[0].text
            cc_data.append({
                'province': province,
                'city':city,
                'num': num
            })
        # 作者
        ci = ci_ht.xpath('//div[@class="AuthorList"]')[0]
        ci = etree.tostring(ci, encoding='utf-8').decode('utf-8')
        ci = ci.replace('\n', '')
        ci = ci.replace('<div class="AuthorList">', '')
        # print(ci)
        dy = ''
        city = ''
        while ci != '':
            if ci[:len(str1)] == str1:
                ci = ci[len(str1):]
                dy = ci.split(str3)[0]
                city = ''
                ci = ci[len(dy) + len(str3):]
            elif ci[:len(str2)] == str2:
                ci = ci[len(str2):]
                city = ci.split(str3)[0]
                ci = ci[len(city) + len(str3):]
            elif ci[:3] == '<a ':
                front = ci.split('author=')[0]
                ci = ci[len(front + 'author='):]
                au_id = ci.split('"')[0]
                ci = ci[len(au_id + str4):]
                au = ci.split('</a>')[0]
                ci = ci[len(au + '</a>'):]
                cit = {
                    'province': province,
                    'city': city,
                    'dynasty': dy,
                    'au_id': au_id,
                    'au': au
                }
                ci_data.append(cit)
            else:
                break


    # print(pr_data)
    pr_df = pd.DataFrame(pr_data)
    pr_df.to_csv("address_province.csv")

    cc_df = pd.DataFrame(cc_data)
    cc_df.to_csv("address_city.csv")

    ci_df = pd.DataFrame(ci_data)
    ci_df.to_csv("address_author.csv")


get_address()
