import json

import requests

from bs4 import BeautifulSoup
from config import URL, HEADERS


def get_lxml(url):
    response = requests.get(url, headers=HEADERS).text
    return BeautifulSoup(response, 'lxml')


def get_data(lxml: BeautifulSoup, level) -> dict:
    return {
        'code': lxml.find('b').text,
        'title': lxml.find('td', class_='name').find('a').text,
        'level': level
    }


def get_bbk(level=1, lxml: BeautifulSoup = get_lxml(URL)):
    data = []
    if level > 5:
        return data
    print(f'------{level}-------')
    bbk_list = lxml.find('table', id='udktable').find('tbody').find_all('tr')
    for item in bbk_list:
        classes = item['class']
        if 'dir' in classes:
            full_url = URL + item.find('a')['href']
            print(full_url)
            context = get_data(item, level)
            context['children'] = get_bbk(level+1, lxml=get_lxml(full_url))
            data.append(context)
        elif 'file' in classes:
            context = get_data(item, level)
            context['children'] = None
            data.append(context)
    return data


def save(data):
    with open("bbk.json", "w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)


def main():
    data = get_bbk()
    save(data)
