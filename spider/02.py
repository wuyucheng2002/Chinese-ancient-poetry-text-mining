# 根据诗作的链接爬取诗作和意象
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


def get_text(xml):
    ts = ''
    for x in xml:
        t = etree.tostring(x, encoding='utf-8').decode('utf-8')
        t = re.sub(pattern='<.+?>', repl='', string=t)
        t = t.replace('\n', '')
        t = t.replace(' ', '')
        ts += t
    return ts


def get_dynasty(dy):
    print(dy)
    df = pd.read_csv('poem_href_' + dy + '.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }

    po_data = []
    im_data = []
    old_id = []
    for index, row in df.iterrows():
        print(index)

        while True:
            try:
                url = 'https://www.sou-yun.cn/Query.aspx?type=poem1&id=' + str(row['po_id'])
                req = requests.get(url, headers=headers)
                req = req.text
                ht = html.fromstring(req)
                # 标题
                title = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]/preceding-sibling::*')
                title = get_text(title)
                # 作者
                author = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="poemAuthor"]')
                author = get_text(author)
                # 类别、押韵
                indent = ht.xpath('//*[@class="poemTitle inDetail"]/*[@class="titleIndent"]')[0].text
                # 内容
                content = ht.xpath('//*[@class="poemContent"]/*')
                content = get_text(content)
                # 意象
                # option = webdriver.ChromeOptions()
                # option.add_argument('headless')
                # driver = webdriver.Chrome(options=option)
                driver = webdriver.Chrome()
                driver.get(url)
                time.sleep(3)
                # wait = ui.WebDriverWait(driver, 10)
                # wait.until(lambda driver: driver.find_element(By.CLASS_NAME, 'popupad-close'))
                WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'popupad-close')))
                driver.find_element(By.CLASS_NAME, 'popupad-close').click()
                time.sleep(1)
                cs = driver.find_elements(By.XPATH, '//*[@class="_poem"]//*[@class="bold"]')
                for c in cs:
                    c.click()
                    time.sleep(0.1)
                time.sleep(3)

                while True:
                    tag = True
                    im_ids = ''
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
                                    im_data.append({
                                        'id': im_id,
                                        'image': im_name,
                                        'explain': exp
                                    })
                    if tag:
                        break

                po = {
                    'po_id': row['po_id'],
                    'au_id': row['au_id'],
                    'title': title,
                    'author': author,
                    'indent': indent,
                    'content': content,
                    'im_ids': im_ids
                }
                po_data.append(po)
                driver.quit()
                break

            except:
                print("error!")

    po_df = pd.DataFrame(po_data)
    po_df.to_csv("poem_" + dy + ".csv")
    im_df = pd.DataFrame(im_data)
    im_df.to_csv("image_" + dy + ".csv")


# get_dynasty('Qin') 'XianQin', 'Qin',, 'Song', 'Liao', 'Jin', 'Yuan', 'Ming', 'Qing'
for dy in ['Han', 'WeiJin', 'NanBei', 'Sui', 'Tang']:
    get_dynasty(dy)


'''
if not im.is_displayed():
    tx = im.get_attribute("innerHTML")
    im_name = tx.split('</div>')[0]
    im_name = re.sub(pattern='<.+?>', repl='', string=im_name)
    exp = re.sub(pattern='<.+?>', repl='', string=tx)
else:
    im_name = im.find_element(By.XPATH, './*[@class="poemTitle"]')
    im_name = im_name.text
    exp = im.text
'''