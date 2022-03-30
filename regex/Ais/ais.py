import re
import requests
import json

# print('load regex.py')
AIS_APPLE = 'https://www.hotdeal.ais.co.th/hotdeal-apple.html'
AIS_SAMSUNG = 'https://www.hotdeal.ais.co.th/hotdeal-samsung.html'
# DTAC = ''
# TRUE = ''

# get <section></section>
section = r'<section class=\"sec_table table_main.*>((.|\n)*?)<\/section>'

# regex pattern
tbody = r"<tbody>((.|\n)*?)<\/tbody>"
txttr = r"<tr>((.|\n)*?)<\/tr>"
# txtmodel = r"<td.*?class=\".*?txtmodel.*?\">(.*?)<\/td>"
# txttype = r"<td.*?class=\".*?txttype.*?\">(.*?)<\/td>"
# txtnormal_price = r"<td.*?class=\".*?txtnormalprice.*?\">(.*?)<\/td>"
# txtspecial_price = r"<td.*?class=\".*?txtspecialprice.*?\">(.*?)<\/td>"
# txtpackage = r"<td.*?class=\".*?bggreen13.*?\">(.*?)<\/td>"

# get number in span
# span = r'<td rowspan="(\w+)" class="fixed txttype'

# get text from tags html
txt = r'[^<>\n]+(?=[<])'

# section is tags and data inside
def get_tbody(section):
    # return list of tbody
    ls = []
    data = re.findall(tbody, section)
    # print(data, len(data))s
    for i in data:
        # print(i[0])
        ls += [i[0]]
    return ls

def get_td(tbody):
    # get td from tr tags 
    # if 'txtmodel' in i: s
    # return list of tr
    tbody = get_tbody(tbody)
    # print(tbody[0], len(tbody))
    ls_tr = []
    for i in tbody:
        # print(i)
        data = re.findall(txttr, i)
        # print(data, len(data))
        ls_tr += [data]
    return ls_tr

def get_text(data_td):
    # print(data_td, len(data_td))
    # print(data_td[0])

    ls_json = []

    # data_td is data from tr
    # list
    for i in data_td:
        model = None
        size = None
        type = None
        normalprice = None
        detail = None
        ls_promotions = []
        type_18 = None
        detail_18 = None
        is_18 = False
        ls_promotions_18 = None
        for j in i:
            data = j[0]
            # print(data)
            ls_text = re.findall(txt, data)
            # print(ls_text)
            if ls_text[-1].strip() == '':
                ls_text.pop()
            if ls_text[-1] == 'ทุกสาขา':
                ls_text.pop()
            # print(ls_text)
            if 'txttype' in data:
                if 'txtmodel' in data:
                    # promotions 12 months
                    # print('promotions 12 months')
                    is_18 = False
                    model  = ls_text.pop(0)
                    size = ls_text.pop(0)
                    type = ls_text.pop(0)
                    detail = ''.join(ls_text[:len(ls_text)-4])
                    normalprice = ls_text[-4]
                    ls_promotions.append({'specialprice' : ls_text[-3], 'paid' : ls_text[-2], 'package' : ls_text[-1],})
                else:
                    # 18 months
                    # print('promotions 18 months -------------------->')
                    is_18 = True
                    ls_promotions_18 = []
                    # print(ls_text)
                    type_18 = ls_text.pop(0)
                    detail_18 = ''.join(ls_text[:len(ls_text)-3])
                    ls_promotions_18.append({'specialprice' : ls_text[-3], 'paid' : ls_text[-2], 'package' : ls_text[-1],})
            else:
                if not is_18:
                    ls_promotions.append({'specialprice' : ls_text[-3], 'paid' : ls_text[-2], 'package' : ls_text[-1],})
                else:
                    # add promotions 18 months
                    ls_promotions_18.append({'specialprice' : ls_text[-3], 'paid' : ls_text[-2], 'package' : ls_text[-1],})

        data_json = {
            'model' : model,
            'size' : size,
            'type' : type,
            'normalprice' : normalprice,
            'detail' : detail,
            'promotions' : ls_promotions,
            'type_18' : type_18,
            'detail_18' : detail_18,
            'promotions_18' : ls_promotions_18,
        }

        # print('model : ',model)
        # print('size : ' ,size)
        # print('type : ', type)
        # print('detail : ', detail)
        # print('normalprice : ', normalprice)
        # print('ls_promotions : ', ls_promotions)
        # if type_18:
        #     print('type_18 : ', type_18)
        # if detail_18:
        #     print('detail_18 : ', detail_18)

        # print(data_json)

        ls_json.append(data_json)
    # print(ls_json, len(ls_json))
    # return json.dumps(ls_json, ensure_ascii=False)\
    return ls_json

def get_text_5(data_td):
    # print(data_td, len(data_td))
    # print(data_td[0])
    def add_data(lst: list, ls_txt: list):
        # add data manage data
        lst.append({'specialprice' : ls_txt[-4], 'paid' : ls_txt[-3], 'package_1' : ls_txt[-1], 'package_2': ls_txt[-2]})

    ls_json = []

    # data_td is data from tr
    # list
    for i in data_td:
        model = None
        size = None
        type = None
        normalprice = None
        detail = None
        ls_promotions = []
        type_18 = None
        detail_18 = None
        is_18 = False
        ls_promotions_18 = None
        for j in i:
            data = j[0]
            # print(data)
            ls_text = re.findall(txt, data)
            # print(ls_text)
            if ls_text[-1].strip() == '':
                ls_text.pop()
            if ls_text[-1] == 'ทุกสาขา':
                ls_text.pop()
            # print(ls_text)
            if 'txttype' in data:
                if 'txtmodel' in data:
                    # promotions 12 months
                    # print('promotions 12 months')
                    is_18 = False
                    model  = ls_text.pop(0)
                    size = ls_text.pop(0)
                    type = ls_text.pop(0)
                    detail = ''.join(ls_text[:len(ls_text)-5])
                    normalprice = ls_text[-5]
                    # ls_promotions.append({'specialprice' : ls_text[-4], 'paid' : ls_text[-3], 'package_1' : ls_text[-1], 'package_2': ls_text[-2]})
                    add_data(ls_promotions, ls_txt=ls_text)
                else:
                    # 18 months
                    # print('promotions 18 months -------------------->')
                    is_18 = True
                    ls_promotions_18 = []
                    # print(ls_text)
                    type_18 = ls_text.pop(0)
                    detail_18 = ''.join(ls_text[:len(ls_text)-3])
                    # ls_promotions_18.append({'specialprice' : ls_text[-4], 'paid' : ls_text[-3], 'package_1' : ls_text[-1], 'package_2': ls_text[-2]})
                    add_data(ls_promotions_18, ls_txt=ls_text)
            else:
                if not is_18:
                    # ls_promotions.append({'specialprice' : ls_text[-4], 'paid' : ls_text[-3], 'package_1' : ls_text[-1], 'package_2': ls_text[-2]})
                    add_data(ls_promotions, ls_txt=ls_text)
                else:
                    # add promotions 18 months
                    # ls_promotions_18.append({'specialprice' : ls_text[-4], 'paid' : ls_text[-3], 'package_1' : ls_text[-1], 'package_2': ls_text[-2]})
                    add_data(ls_promotions_18, ls_txt=ls_text)

        data_json = {
            'model' : model,
            'size' : size,
            'type' : type,
            'normalprice' : normalprice,
            'detail' : detail,
            'promotions' : ls_promotions,
            'type_18' : type_18,
            'detail_18' : detail_18,
            'promotions_18' : ls_promotions_18,
        }

        # print('model : ',model)
        # print('size : ' ,size)
        # print('type : ', type)
        # print('detail : ', detail)
        # print('normalprice : ', normalprice)
        # print('ls_promotions : ', ls_promotions)
        # if type_18:
        #     print('type_18 : ', type_18)
        # if detail_18:
        #     print('detail_18 : ', detail_18)

        # print(data_json)

        ls_json.append(data_json)
    # print(ls_json, len(ls_json))
    # return json.dumps(ls_json, ensure_ascii=False)\
    return ls_json
def get_iphone(number):
    print(f'Hello get_iphone!!! index = {number}')
    page = requests.get(AIS_APPLE)
    page.encoding = 'utf-8'
    # print('After requests')
    # print(page.text)
    # sh = section
    package = re.findall(section, page.text)
    # print(package[0][0], len(package))

    # print(len(package))
    # len package = 5
    # iphone13 = package[0][0]
    # iphonese = package[1][0]
    # iphone_5g = package[2][0]
    # iphone_4g = package[3][0]
    # ipad = package[4][0]
    data_td = get_td(package[number][0])
    if number == 4:
        data = get_text_5(data_td)
    else:
        data = get_text(data_td)
    # return json.dumps(data, ensure_ascii=False)
    return data

# s = get_iphone(0)
# print(s)
# with open('AIS_APPLE.json', 'w', encoding='utf-8') as writefile:
#     json.dump(s, writefile, ensure_ascii=False)
# print('Done writing json')
# print(s)