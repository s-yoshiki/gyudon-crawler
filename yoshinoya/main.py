from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re
import requests
import time
import math
import urllib.parse

# global vars
base_url = 'https://www.yoshinoya.com'
csv_path='./menu.csv'

# メニュー大分類
def get_menu_urls():
    return [
        "https://www.yoshinoya.com/menu/gyudon",
        "https://www.yoshinoya.com/menu/gyunonabeyaki",
        "https://www.yoshinoya.com/menu/wset",
        "https://www.yoshinoya.com/menu/karaage",
        "https://www.yoshinoya.com/menu/mixfly",
        "https://www.yoshinoya.com/menu/gyukarubidon",
        "https://www.yoshinoya.com/menu/set",
        "https://www.yoshinoya.com/menu/unajyu",
        "https://www.yoshinoya.com/menu/curry",
        "https://www.yoshinoya.com/menu/morningset",
        "https://www.yoshinoya.com/menu/ichijyu-sansai-asazen",
        "https://www.yoshinoya.com/menu/butadon",
        "https://www.yoshinoya.com/menu/kids",
        "https://www.yoshinoya.com/menu/sidemenu",
        "https://www.yoshinoya.com/menu/yoshinomi",
    ]

# メニュー小分類
def extract_detail_urls(url):
    result = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    soup = soup.select('li.menu-content')
    for elm in soup:
        if len(elm.select('a')) == 0:
            continue
        result.append(elm.find('a')['href'])
    return result

# 数字抽出
def extract_num(src):
    return re.sub('\\D', '', src)

if __name__ == "__main__":
    parent_urls = get_menu_urls()
    contents_url = []
    for child_url in parent_urls:
        urls = extract_detail_urls(child_url)
        for url in urls:
            contents_url.append(url)
    contents_url = sorted(set(contents_url), key=contents_url.index)
    result = []
    product_id = 0
    uid = 0
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'uid', 'product_id', 'category',  'title', 'size', 'price', 'calorie', 'desc', 'url','image'
        ])
        for url in contents_url:
            if len(url.split('/')) != 7:
                continue
            # Id
            product_id += 1
            # category
            print(url)
            category = url.split('/')[4]
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            title = ''
            image = ''
            desc = ''
            size = ''
            price = ''
            calorie = ''
            # title
            title = soup.find('h1').get_text()
            # image
            if len(soup.select('.detailmenu-img')) > 0:
                image = soup.select('.detailmenu-img')[0].find('img')['src']
            # desc
            if len(soup.select('div.text')) > 0:
                desc = soup.select('div.text')[0].get_text().strip()
            # item detail
            elems = soup.select('table.price-list')[0].select('tr')
            for elem in elems:
                uid += 1
                # size
                if len(elem.select('.menu-size')) > 0:
                    # print(elem)
                    size = elem.select('.menu-size')[0].get_text().strip()
                # price
                if len(elem.select('.menu-price')) > 0:
                    price = elem.select('.menu-price')[0].get_text().strip()
                    price = extract_num(price)
                # calorie
                if len(elem.select('.menu-calorie')) > 0:
                    calorie_raw = elem.select('.menu-calorie')[0].get_text().strip()
                    calorie = extract_num(calorie_raw)
                row = [
                    uid, product_id, category, title, size, price, calorie, desc, url, image
                ]
                writer.writerow(row)
    # sidemenu
    with open(csv_path, 'a') as f:
        writer = csv.writer(f)
        urls = [
            "https://www.yoshinoya.com/menu/yoshinomi",
            "https://www.yoshinoya.com/menu/sidemenu",
        ]
        for url in urls:
            res = requests.get(url)
            category = url.split('/')[4]
            soup = BeautifulSoup(res.text, 'html.parser')
            elems = soup.select('ul.categorymenu-area-list')[0].select('li.menu-content')
            for elem in elems:
                if len(elem.select('a')) > 0:
                    continue
                product_id += 1
                uid += 1
                title = ''
                image = ''
                desc = ''
                size = ''
                price = ''
                calorie = ''
                desc = ''

                # title
                title = elem.find('h3').get_text()
                # image
                image = elem.find('img')['src']
                # price
                price = elem.select('span.menu-price')[0].get_text()
                price = extract_num(price)
                # calorie
                if len(elem.select('span.menu-calorie')) > 0:
                    calorie = elem.select('span.menu-calorie')[0].get_text()
                    calorie = extract_num(calorie)
                row = [
                    uid, product_id, category, title, size, price, calorie, desc, url, image
                ]
                writer.writerow(row)