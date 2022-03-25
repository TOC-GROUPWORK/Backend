import re
import requests
import json

AIS_APPLE = 'https://www.hotdeal.ais.co.th/hotdeal-apple.html'
AIS_SAMSUNG = 'https://www.hotdeal.ais.co.th/hotdeal-samsung.html'
DTAC = ''
TRUE = ''

URL = AIS_APPLE

def add_data(regex, item, list: list):
    data = re.findall(regex, item)
    list.append(get_text(''.join(data)))

def get_text(item):
    html_get = r"[^<>()]+(?=[<])"
    data = re.findall(html_get, item)
    return ''.join(data)

print('Hello regex!!!')
page = requests.get(URL)
page.encoding = 'utf-8'
# print(page.text)

# f = open('ais.txt', 'a')
# f.write(page.text)
# f.close()
# f = open('test2.txt', 'r')
# print(f.read())

# get <section></section>
section = r'<section class=\"sec_table table_main.*>((.|\n)*?)<\/section>'

tbody = r"<tbody>((.|\n)*?)<\/tbody>"
txttr = r"<tr>((.|\n)*?)<\/tr>"
txtmodel = r"<td.*?class=\".*?txtmodel.*?\">(.*?)<\/td>"
txttype = r"<td.*?class=\".*?txttype.*?\">(.*?)<\/td>"
txtnormal_price = r"<td.*?class=\".*?txtnormalprice.*?\">(.*?)<\/td>"
txtspecial_price = r"<td.*?class=\".*?txtspecialprice.*?\">(.*?)<\/td>"
txtpackage = r"<td.*?class=\".*?bggreen13.*?\">(.*?)<\/td>"
# get number in span
span = r'<td rowspan="(\w+)" class="fixed txttype'
# get text from tags html
txt = r'[^<>\n]+(?=[<])'

sh = section
package = re.findall(sh, page.text)
# print(package[0][0], len(package))

print(len(package))
# len package = 4
iphone13 = package[0][0]
iphonese = package[1][0]
iphone_5g = package[2][0]
iphone_4g = package[3][0]
ipad = package[4][0]

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
            print(ls_text)
            if ls_text[-1].strip() == '':
                ls_text.pop()
            if ls_text[-1] == 'ทุกสาขา':
                ls_text.pop()
            print(ls_text)
            if 'txttype' in data:
                if 'txtmodel' in data:
                    # promotions 12 months
                    print('promotions 12 months')
                    is_18 = False
                    model  = ls_text.pop(0)
                    size = ls_text.pop(0)
                    type = ls_text.pop(0)
                    detail = ''.join(ls_text[:len(ls_text)-4])
                    normalprice = ls_text[-4]
                    ls_promotions.append({'specialprice' : ls_text[-3], 'paid' : ls_text[-2], 'package' : ls_text[-1],})
                else:
                    # 18 months
                    print('promotions 18 months -------------------->')
                    is_18 = True
                    ls_promotions_18 = []
                    print(ls_text)
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

        print(data_json)

        ls_json.append(data_json)
    # print(ls_json, len(ls_json))
    return json.dumps(ls_json, ensure_ascii=False)

def get_info(section):
    #  get text from tags
    #  return list
    data = re.findall(tbody, section)
    # print(data, len(data))
    ls = []
    for i in data:
        ls += [re.findall(txt, i[0])]
    return ls

def to_json(list):
    err = 0
    for i in list:
        print(i, len(i))
        if len(i) == 35:
            model = i[0]
            storage = i[1]
            type = [i[2]]
            details = [''.join(i[3:5])]
            normal_price = i[6]
            promotions = []
            # promotions += [i[7], i[8], [9]]
            for j in range(4):
                num = j * 3
                promotions += [i[num + 7], i[num + 8], i[num + 9]]

            type += i[19]
            details += ''.join(i[20:22])
            for j in range(4):
                num = j*3
                promotions += [i[num + 23], i[num + 24], i[num + 25]]
        elif len(i) == 18:
            print('18')
        else:
            err += 1
            print('error', err)

def version_1():
    sh = get_info(iphone_5g)
    print(sh, len(sh))
    print('--------------------------')
    to_json(sh)

def version_2():
    data_td = get_td(iphone_5g)
    return get_text(data_td)

s = version_2()
# print(s)