import re
import requests

print('Hello Dtac!!!')
DTAC_BASE = 'https://www.dtac.co.th/'
# DTAC_APPLE = 'https://www.dtac.co.th/apple/'
APPLE = 'apple/'


txt_product = r'<div class="item-mobile product"((.|\n)*?)<ul class="txt-body-s">((.|\n)*?)<\/div>'
txt_sprice = r'data-price="(.*)" '
txt_name = r'data-name="(.*)"'
txt_price = r'<u>(.*)?<\/u>'
txt_detail = r'<li>(.*)?<\/li>'
# txt_detail2 = r'<li>(.*)?<\/li>\t'
txt = r'[^<>\n\t]+(?=[<])'

def apple():
    page = requests.get(DTAC_BASE + APPLE)
    page.encoding = 'utf-8'

    # print(page.text)

    card = re.findall(txt_product, page.text)
    # print('card len = ', len(card))
    # print('card[0] len = ', len(card[0]))
    ls_json = []

    for product in card:
        data = product[0]
        sprice = re.findall(txt_sprice, data)
        name = re.findall(txt_name, data)
        price = re.findall(txt_price, data)
        detail = re.findall(txt_detail, data)
        detail += re.findall(txt, product[2])

        # print(data)
        # print(product[2])

        # print(sprice)
        # print(name)
        # print(price)
        # print(detail)

        data_json = {
            'model': name[0],
            'specialprice': sprice[0],
            'normalprice': price[0],
            'detail': detail,
        }

        print(data_json)
        ls_json.append(data_json)
    
    return ls_json

def samsung():
    pass

def scraping(brand):
    page = requests.get(DTAC_BASE + '/' + brand + '/')
    page.encoding = 'utf-8'

    # print(page.text)

    card = re.findall(txt_product, page.text)
    # print('card len = ', len(card))
    # print('card[0] len = ', len(card[0]))
    ls_json = []

    for product in card:
        data = product[0]
        sprice = re.findall(txt_sprice, data)
        name = re.findall(txt_name, data)
        price = re.findall(txt_price, data)
        detail = re.findall(txt_detail, data)
        detail += re.findall(txt, product[2])

        # print(data)
        # print(product[2])

        # print(sprice)
        # print(name)
        # print(price)
        # print(detail)
        data_json = {
            'model': name[0],
            'specialprice': sprice[0],
            'normalprice': price[0],
            'detail': detail,
        }

        print(data_json)
        ls_json.append(data_json)
    
    return ls_json

# apple()
# scraping('samsung')