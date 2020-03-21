from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re
import requests
import time
import math
import urllib.parse

# global vars
base_url = 'https://www.sukiya.jp'
csv_path='./menu.csv'

# メニュー大分類
def get_menu_urls():
    return [
        "https://www.sukiya.jp/menu/in/gyudon/",
        "https://www.sukiya.jp/menu/in/gyusuki/",
        "https://www.sukiya.jp/menu/in/curry/",
        "https://www.sukiya.jp/menu/in/don/",
        "https://www.sukiya.jp/menu/in/special/",
        "https://www.sukiya.jp/menu/in/kids/",
        "https://www.sukiya.jp/menu/in/side/",
        "https://www.sukiya.jp/menu/in/drink/",
    ]

# メニュー小分類
def extract_detail_urls(url):
    result = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    soup = soup.select('div.sec_product_table')[0].select('a')
    for elm in soup:
        result.append(base_url + elm['href'])
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
        # sleep(1)
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
            soup = BeautifulSoup(res.text, 'html.parser')
            # title
            title = soup.find('h1').get_text()
            # image
            elems = soup.select('.vi_img')
            for elem in elems:
                image = base_url + soup.find('img')['src']
            # desc
            desc = soup.select('p.product_lead')[0].get_text().replace('\n', '\\n')
            # item detail
            elems = soup.select('#sec_dish_nums')[0].select('li')
            for elem in elems:
                uid += 1
                # size
                size = elem.find('dt').get_text().strip()
                # price
                price = elem.select('dd.price')[0].find('em').get_text().strip()
                price = get_price_without_tax(int(price))
                # calorie
                calorie_raw = elem.select('dd.calorie')[0].get_text().strip()
                calorie = extract_num(calorie_raw)
                row = [
                    uid, product_id, category, title, size, price, calorie, desc, url, image
                ]
                writer.writerow(row)