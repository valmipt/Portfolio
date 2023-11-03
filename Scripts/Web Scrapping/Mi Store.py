import csv
import json

import requests

file_name = 'mi_getapps_dump.csv'


def open_csv(file):
    writer = csv.writer(file)
    writer.writerow(
        ['ID', 'Name', 'Category', 'Company name', 'Version name', 'Version code', 'Installs', 'Rating']
    )


def write_to_csv(file, category, apps):
    category_name = category['categoryName']
    writer = csv.writer(file)
    for app in apps:
        writer.writerow(
            [
                app['packageName'],
                app['displayName'],
                category_name,
                app['publisherName'],
                app['versionName'],
                app['versionCode'],
                app['downloadCount'],
                app['ratingScore'],
            ]
        )


def get_apps(category):
    category_name = category['categoryName']
    print(f'Getting {category_name} apps')
    category_id = category['categoryId']
    try:
        resp = requests.get(f'https://global.app.mi.com/intl/web/api/category/{category_id}?page=1&lo=RU&la=ru')
        return json.loads(resp.text)['list'][0]['data']['listApp']
    except requests.RequestException as request_error:
        print(request_error)
        return []
    except json.decoder.JSONDecodeError as json_error:
        print(json_error)
        print(json_error.doc)
        return []


def get_categories(category_type):
    print(f'Getting {category_type} categories')
    try:
        resp = requests.get(f'https://global.app.mi.com/intl/web/api/category/list?type={category_type}&lo=RU&la=ru')
        return json.loads(resp.text)['tabList']
    except requests.RequestException as request_error:
        print(request_error)
        return []
    except json.decoder.JSONDecodeError as json_error:
        print(json_error)
        print(json_error.doc)
        return []


def main():
    main_categories = get_categories('main')
    game_categories = get_categories('games')
    with open(file_name, mode='w', encoding='utf-8') as file:
        open_csv(file)

        for category in main_categories:
            apps = get_apps(category)
            write_to_csv(file, category, apps)

        for category in game_categories:
            apps = get_apps(category)
            write_to_csv(file, category, apps)

        print("Finished")


if __name__ == '__main__':
    main()
