from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re
import requests
import time
import math
import urllib.parse

# global vars
base_url = 'https://www.matsuyafoods.co.jp/'
csv_path='./menu.csv'

# メニュー大分類
def get_menu_urls():
    return [
        "https://www.matsuyafoods.co.jp/matsuya/menu/pre_gyuu/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/gyumeshi/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/curry/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/don/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/teishoku/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/morning/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/okosama/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/udoon/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/yorumatsu/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/sidemenu/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/topping/index.html",
        "https://www.matsuyafoods.co.jp/matsuya/menu/drink/index.html",
    ]

# メニュー小分類
def extract_detail_urls(url):
    result = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    soup = soup.select('section.section-main-cmn')[0].select('a.item-menu-cmn')
    for elm in soup:
        path = elm['href'].replace('menu/../', '')
        result.append(path)
    return result

# 数字抽出
def extract_num(src):
    return re.sub('\\D', '', src)

# 税抜き
def get_price_without_tax(num):
    return math.ceil(num / 1.10) 

if __name__ == "__main__":
    parent_urls = get_menu_urls()
    contents_url = []
    for child_url in parent_urls:
        urls = extract_detail_urls(child_url)
        for url in urls:
            contents_url.append(url)
    contents_url = sorted(set(contents_url), key=contents_url.index)
    result = []
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'uid', 'product_id', 'category',  'title', 'size', 'price', 'calorie', 'desc', 'url','image'
        ])
        product_id = 0
        uid = 0
        for url in contents_url:
            # Id
            product_id += 1
            # category
            category = url.split('/')[5]
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            # title
            title = soup.find('h1').get_text()
            # image
            if len(soup.select('div.article-thumb')[0]) > 0:
                image = soup.select('div.article-thumb')[0].find('img')['src']
            # desc
            desc =''
            if len(soup.select('p.leadTxt')) > 0:
                desc = soup.select('p.leadTxt')[0].get_text().replace('\n', '\\n')
            # item detail
            elems = soup.select('div.nourishment')[0].select('li')
            calories = {'':''}
            for elem in elems:
                key = ''
                if len(elem.select('h3')) > 0:
                    key = elem.select('h3')[0].get_text()
                if len(elem.select('p')) > 0:
                    calories[key] = extract_num(
                        elem.find('p').get_text().split('kcal')[0]
                    )
            elems = soup.select('ul.ul-text')[0].select('li')
            for elem in elems:
                uid += 1
                calorie = ''
                size = ''
                # size
                if len(elem.select('p.th')) > 0:
                    size = elem.select('p.th')[0].get_text().strip()
                # price
                price = elem.select('p.td')[0].select('span.clr')[0].get_text().strip()
                price = get_price_without_tax(int(price))
                row = [
                    uid, product_id, category, title, size, price, calorie, desc, url, image
                ]
                # calorie
                if size == 'ライスミニ':
                    calorie = calories['']
                else:
                    calorie = calories[size]
                row = [
                    uid, product_id, category, title, size, price, calorie, desc, url, image
                ]
                writer.writerow(row)