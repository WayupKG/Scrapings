import requests
import json

from bs4 import BeautifulSoup

from data.config import URL, HEADERS


def get_item_data_theme(parent_id, item, children) -> dict[str: str]:
    context = dict()
    title = item.find('a')
    if not title:
        title_span = item.find('span', {'data-parent': item.get('id')})
    else:
        titles = title.text.split(' ')
        titles.pop()
    context['id'] = parent_id
    context['title'] = " ".join(titles) if title else title_span.text
    context['depth'] = item.get('data-depth')
    context['children'] = children
    return context


def get_soup():
    response = requests.get(URL, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    return soup


def get_theme(depth=1, soup=get_soup(), parent_id=None):
    data = []
    if depth > 5:
        return data
    themes_list = soup.find("ul", class_='folder__sub')
    theme_item = themes_list.find_all("li", {'data-depth': depth}, class_="folder__item")
    for num, item in enumerate(theme_item, 1):
        children = None
        if parent_id:
            current_id = f'{parent_id}.{num}'
        else:
            current_id = str(num)
        if 'no-child' not in item['class']:
            children = get_theme(depth+1, soup=item, parent_id=current_id)
        data.append(get_item_data_theme(current_id, item, children))
    return data


def save(data):
    with open("bbk.json", "w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False)


def main():
    data = get_theme()
    print(len(data))
    save(data)
