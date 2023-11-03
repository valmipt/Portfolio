import csv
import textwrap

import requests
from bs4 import BeautifulSoup

file_name = 'galaxy_dump.csv'


def open_csv(file):
    writer = csv.writer(file)
    writer.writerow(
        ['ID', 'Name', 'Category', 'Company name', 'Version name', 'Version code', 'Installs', 'Rating']
    )


def write_to_csv(file, apps):
    writer = csv.writer(file)
    for app in apps:
        writer.writerow(
            [
                app['packageName'],
                app['displayName'],
                app['categoryName'],
                app['publisherName'],
                app['versionName'],
                app['versionCode'],
                app['downloadCount'],
                app['ratingScore'],
            ]
        )


def get_apps(category, start=1, end=100):
    category_id = category['id']
    category_name = category['name']
    print(f'Getting {category_name} apps')
    try:
        resp = requests.post(
            url='https://galaxystore.samsung.com/storeserver/ods.as?id=categoryProductList2Notc',
            headers={
                'x-galaxystore-url': 'http://ru-odc.samsungapps.com/ods.as',
            },
            data=textwrap.dedent(f'''\
                <?xml version="1.0" encoding="UTF-8"?>
                <SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">
                <request name="categoryProductList2Notc" id="2030" numParam="10" transactionId="10a4ee19e126"> 
                    <param name="imgWidth">135</param>
                    <param name="startNum">{start}</param>
                    <param name="imgHeight">135</param>
                    <param name="alignOrder">bestselling</param>
                    <param name="contentType">All</param>
                    <param name="endNum">{end}</param>
                    <param name="categoryName">{category_name}</param>
                    <param name="categoryID">{category_id}</param>
                    <param name="srcType">01</param>
                    <param name="status">0</param>
                </request>
                </SamsungProtocol>''').encode('utf-8'),
        )
        app_list = []
        for app_xml in BeautifulSoup(resp.text, features='xml').SamsungProtocol.response.findAll("list"):
            app_list.append({
                'packageName': app_xml.find("value", {'name': 'GUID'}).contents[0],
                'displayName': app_xml.find("value", {'name': 'productName'}).contents[0],
                'categoryName': app_xml.find("value", {'name': 'categoryName'}).contents[0],
                'publisherName': app_xml.find("value", {'name': 'sellerName'}).contents[0],
                'versionName': app_xml.find("value", {'name': 'version'}).contents[0],
                'versionCode': app_xml.find("value", {'name': 'versionCode'}).contents[0],
                'downloadCount': '?',
                'ratingScore': '?',
            })

        return app_list
    except requests.RequestException as request_error:
        print(request_error)
        return []
    except Exception as error:
        print('Generic error')
        print(error)
        return []


def get_categories(category_type):
    if category_type == 'games':
        xml_param = '<param name="upLevelCategoryKeyword">Games</param>'
    elif category_type == 'apps':
        xml_param = '<param name="gameCateYN">N</param>'
    else:
        print('Unknown category. use "apps" or "games"')
        return []
    print(f'Getting {category_type} categories')
    try:
        resp = requests.post(
            url='https://galaxystore.samsung.com/storeserver/ods.as?id=normalCategoryList',
            headers={
                'x-galaxystore-url': 'http://ru-odc.samsungapps.com/ods.as',
            },
            data=textwrap.dedent(f'''\
                <?xml version="1.0" encoding="UTF-8"?><SamsungProtocol networkType="0" version2="0" lang="EN" openApiVersion="28" deviceModel="SM-G998B" storeFilter="themeDeviceModel=SM-G998B_TM||OTFVersion=8000000||gearDeviceModel=SM-G998B_SM-R800||gOSVersion=4.0.0" mcc="450" mnc="00" csc="CPW" odcVersion="4.5.21.6" version="6.5" filter="1" odcType="01" systemId="1604973510099" sessionId="10a4ee19e202011101104" logId="XXX" userMode="0">
                    <request name="normalCategoryList" id="2225" numParam="4" transactionId="10a4ee19e011">
                      <param name="needKidsCategoryYN">Y</param>
                      <param name="imgWidth">135</param>
                      <param name="imgHeight">135</param>
                      {xml_param}
                    </request>
                </SamsungProtocol>''').encode('utf-8'),
        )
        category_list = []
        for app_xml in BeautifulSoup(resp.text, features='xml').SamsungProtocol.response.findAll("list"):
            category_list.append(dict(
                id=app_xml.find("value", {'name': 'categoryID'}).contents[0],
                name=app_xml.find("value", {'name': 'categoryName'}).contents[0],
            ))

        return category_list
    except requests.RequestException as request_error:
        print(request_error)
        return []
    except Exception as error:
        print('Generic error')
        print(error)
        return []


def main():
    apps_categories = get_categories('apps')
    games_categories = get_categories('games')
    with open(file_name, mode='w', encoding='utf-8') as file:
        open_csv(file)

        for category in apps_categories:
            apps = get_apps(category)
            write_to_csv(file, apps)

        for category in games_categories:
            apps = get_apps(category)
            write_to_csv(file, apps)

        print("Finished")


if __name__ == '__main__':
    main()
