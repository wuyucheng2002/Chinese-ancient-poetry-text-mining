# 抓取补充诗词和意象
import requests
from lxml import html
from lxml import etree
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_dynasty(dy):
    def get_text(xml):
        ts = ''
        for x in xml:
            t = etree.tostring(x, encoding='utf-8').decode('utf-8')
            t = re.sub(pattern='<.+?>', repl='', string=t)
            t = t.replace('\n', '')
            t = t.replace(' ', '')
            ts += t
        return ts

    print(dy)
    df = pd.read_csv('sort_poem_' + dy + '.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    po_data = []
    im_data = []
    old_id = []
    for index, row in df.iterrows():
        print(index, row['name'])
        while True:
            try:
                url = 'https://sou-yun.cn/PoemIndex.aspx?dynasty=' + dy + '&author=' + str(row['id'])
                req = requests.get(url, headers=headers)
                req = req.text
                ht = html.fromstring(req)
                length = len(ht.xpath('//div[@class="poem"]/select/*'))
                break
            except:
                print(0, 'page-error!')

        for i in range(1, length):
            print('page ', i)
            while True:
                try:
                    new_url = url + '&page=' + str(i)
                    req = requests.get(new_url, headers=headers)
                    req = req.text
                    ht = html.fromstring(req)
                    items = ht.xpath('//*[@class ="_poem"]')
                    po_list = []
                    for item in items:
                        po_id = item.attrib['id']
                        po_id = po_id.split("_")[1]
                        po_list.append(po_id)
                    break
                except:
                    print(i, 'page-error!')

            for po_id in po_list:
                po_url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + po_id
                while True:
                    try:
                        req = requests.get(po_url, headers=headers).text
                        ht = html.fromstring(req)
                        break
                    except:
                        print('***')
                # 标题
                title = ht.xpath('//*[@class="poemTitle inDetail"]')[0]
                t = etree.tostring(title, encoding='utf-8').decode('utf-8')
                t = t.split('<span class="poemAuthor">')[0]
                t = re.sub(pattern='<.+?>', repl='', string=t)
                t = t.replace('\n', '')
                t = t.replace(' ', '')
                title = t
                # 作者
                author = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]')
                author = get_text(author)
                ndy = author.split('·')[0]
                au = author.split('·')[1]
                # 类别、押韵
                indent = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="titleIndent"]')[0].text
                genre = ''
                rhyme = ''
                resource = ''
                if not pd.isna(indent):
                    indent = indent.strip()
                    ind_list = indent.split()
                    for ind in ind_list:
                        if '出处：' in ind:
                            resource = ind
                        elif '押' in ind:
                            rhyme = ind
                        else:
                            genre = ind
                # 内容
                content = ht.xpath('//*[@class="poemContent"]/*')
                content = get_text(content)

                while True:
                    tag = True
                    im_ids = ''
                    # 意象
                    try:
                        option = webdriver.ChromeOptions()
                        option.add_argument('headless')
                        driver = webdriver.Chrome(options=option)
                        # driver = webdriver.Chrome()
                        driver.get(po_url)
                        time.sleep(3)
                        WebDriverWait(driver, 30, 0.5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'popupad-close')))
                        driver.find_element(By.CLASS_NAME, 'popupad-close').click()
                        time.sleep(1)
                        cs = driver.find_elements(By.XPATH, '//*[@class="_poem"]//*[@class="bold"]')
                        for c in cs:
                            c.click()
                            time.sleep(0.1)
                        time.sleep(3)

                        driver.implicitly_wait(30)
                        ims = driver.find_elements(By.XPATH, '//*[@class="_poem"]//*[@class="poemNote"]')

                        for im in ims:
                            long_id = im.get_attribute('id')
                            if 'poem_' in long_id and '_comment_Word' in long_id:
                                im_id = long_id.split('_comment_Word')[1]
                                im_ids += im_id + ','
                                if im_id not in old_id:
                                    tx = im.get_attribute("innerHTML")
                                    im_name = tx.split('</div>')[0]
                                    im_name = re.sub(pattern='<.+?>', repl='', string=im_name)
                                    exp = re.sub(pattern='<.+?>', repl='', string=tx)
                                    if im_name == '数据查询中……':
                                        tag = False
                                    else:
                                        old_id.append(im_id)
                                        if '分类：' in exp:
                                            behind = exp.split('分类：')[-1]
                                            exp = exp[len(im_name): - len('分类：' + behind)]
                                        else:
                                            exp = exp[len(im_name): -1]
                                        exp = exp.replace(' ', '')
                                        if '拼音：' in im_name:
                                            pron = im_name.split('拼音：')[1]
                                            im_name = im_name[: - len('拼音：' + pron)]
                                        else:
                                            pron = ''
                                        res = im_name.split("》")[0] + '》'
                                        im_name = im_name[len(res + '：'):]
                                        im_name= im_name.strip()

                                        if '（' in im_name:
                                            im_name = im_name.split('（')[0]

                                        im_data.append({
                                            'id': im_id,
                                            'image': im_name,
                                            'pronunciation': pron,
                                            'resource': res,
                                            'explain': exp
                                        })

                        driver.quit()
                        if tag:
                            break
                    except:
                        print('selenium-error!')

                new_po = {
                    'po_id': po_id,
                    'au_id': row['id'],
                    'title': title,
                    'dynasty': ndy,
                    'class': dy,
                    'author': au,
                    'genre': genre,
                    'rhyme': rhyme,
                    'resource': resource,
                    'content': content,
                    'im_ids': im_ids
                }
                print(new_po)
                po_data.append(new_po)

    po_df = pd.DataFrame(po_data)
    po_df.to_csv("poem_" + dy + "_.csv")
    im_df = pd.DataFrame(im_data)
    im_df.to_csv("image_" + dy + "_.csv")


# get_dynasty('Qin') , 'Qin', 'Han',  'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing'
for dy in ['NanBei', 'Sui', 'Tang']:
    get_dynasty(dy)


