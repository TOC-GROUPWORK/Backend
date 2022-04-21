import re
import requests

print('Hello Dtac!!!')
DTAC_BASE = 'https://www.dtac.co.th/'

txt = r'[^<>\n\t\s]+(?=[<])'

def get_model13(path):
    apple_base = DTAC_BASE + 'apple'

    page = requests.get(apple_base + path)
    page.encoding = 'utf-8'
    if page:
        print('Get page!!!')

    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>((.|\n)*?)<\/table>((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th tH5 tH3 fDtacB">(.*)<\/div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'
    test = r''

    def get_data(data):
        model = None
        size = None
        detail = None
        contact = None
        price_list = []
        model = re.findall(txt_model, data)
        # print('model = ',model)
        if model != []:
            size = re.findall(txt_size, model[0])
            # print(size)

        det = re.findall(txt_detail, data)
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print(detail)
            contact = re.findall(txt_contact, detail)
            # print(contact)
        tbody = re.findall(txt_tbody, data)
        # print('tbody = ',tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            # print('price = ', price)
            price_list.append({
                'package_price': price[0],
                'advance_fee':price[1], 
                'dtac_price': price[2],
                'gold_price': price[3], 
                'platinum_price': price[4],
                # 'contact' : contact,
                # 'detail' : detail,
                })
            # print(price_list, len(price_list))
        
        return {
            'model' : model,
            'size' : size,
            'package' : [
                {
                    'contact' : contact,
                    'detail' : detail,
                    'promotions' : price_list,
                }
            ]
        }

    raw_data = re.findall(txt_raw, page.text)
    print('len raw_data = ', len(raw_data))

    # data in 0, 2, 4 
    print('len raw_data[0] = ', len(raw_data[0]))
    # print(raw_data[0][2])

    ls_json = []

    for data in raw_data:
        js = get_data(data[0])
        
        contact = None
        detail = None
        price_list = []

        det = re.findall(txt_detail, data[2])
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print(detail)
            contact = re.findall(txt_contact, detail)
            # print(contact)
        tbody = re.findall(txt_tbody, data[2])
        # print(tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            price_list.append({
                'package_price': price[0],
                'advance_fee': None, 
                'dtac_price': price[1],
                'gold_price': price[2], 
                'platinum_price': price[3],
                # 'contact' : contact,
                # 'detail' : detail,
                })
            # print(price_list, len(price_list))
        
        # print(js['package'], len(js['package']))
        js['package'] += [{
            'contact' : contact,
            'detail' : detail,
            'promotions' : price_list,
        }]
        # print(js['package'], len(js['package']))

        ls_json.append(js)
        
    print(ls_json, len(ls_json))

    return ls_json

def get_model12(path):
    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th txt-h-2 -bold">(.*)<\/div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'

    apple_base = DTAC_BASE + 'apple'
    page = requests.get(apple_base + path)
    page.encoding = 'utf-8'
    if page:
        print('Get page!!!')

    raw_data = re.findall(txt_raw, page.text)
    print('len raw_data = ', len(raw_data)) # len = 8
    # print(raw_data[0])
    # data in 0
    print('len raw_data[0] = ', len(raw_data[0]))
    # print(raw_data[0][0])
    # for i in raw_data[0]:
    #     print('---->>>>>')
    #     print(i)

    ls_json = []
    for data in raw_data:
        model = None
        size = None
        detail = None
        contact = None
        promotions = []
        model = re.findall(txt_model, data[0])
        print('model = ',model)
        if model != []:
            size = re.findall(txt_size, model[0])
            print(size)
        
        det = re.findall(txt_detail, data[0])
        if det == []:
            det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            if deta == []:
                deta = det[0][0]
            # print(deta)
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print('detail = ',detail)
            contact = re.findall(txt_contact, detail)
            if contact is None or contact == []:
                contact = '(สัญญา 24 เดือน)'
            # print(contact)
        
        tbody = re.findall(txt_tbody, data[0])
        # print(tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            promotions.append({
                'package_price': price[0],
                'advance_fee': price[3], 
                'dtac_price': price[1],
                'gold_price': price[2], 
                'platinum_price': price[2],
                # 'contact' : contact,
                # 'detail' : detail,
                })
            print(promotions, len(promotions))

        ls_json.append({
            'model' : model[0],
            'size' : size[0],
            'package' : [
                {
                    'contact' : contact,
                    'detail' : detail,
                    'promotions' : promotions,
                }
            ]
        })

    ls_json.pop(0)
    ls_json.pop(0)
    ls_json.pop(0)

    # print(ls_json, len(ls_json))

    # for i in ls_json:
    #     print(i)
    #     print()
    return ls_json

def get_modelse(path):
    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th tH5 tH3 fDtacB">(.*)</div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'

    apple_base = DTAC_BASE + 'apple'
    page = requests.get(apple_base + path)
    page.encoding = 'utf-8'
    if page:
        print('Get page!!!')

    raw_data = re.findall(txt_raw, page.text)
    # print('len raw_data = ', len(raw_data)) # len = 8
    # print(raw_data[0])
    # data in 0
    # print('len raw_data[0] = ', len(raw_data[0]))

    ls_json = []

    for data in raw_data:
        model = None
        size = None
        detail = None
        contact = None
        promotions = []
        model = re.findall(txt_model, data[0])
        # print('model = ',model)
        if model != []:
            size = re.findall(txt_size, model[0])
            print(size)
        
        det = re.findall(txt_detail, data[0])
        if det == []:
            det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            if deta == []:
                deta = det[0][0]
            # print(deta)
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print('detail = ',detail)
            contact = re.findall(txt_contact, detail)
            if contact is None or contact == []:
                contact = '(สัญญา 24 เดือน)'
            # print(contact)
        
        tbody = re.findall(txt_tbody, data[0])
        # print(tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            promotions.append({
                'package_price': price[0],
                'advance_fee': price[1], 
                'dtac_price': price[2],
                'gold_price': price[3], 
                'platinum_price': price[4],
                })
            # print(promotions, len(promotions))

        ls_json.append({
            'model' : model[0],
            'size' : size[0],
            'package' : [
                {
                    'contact' : contact,
                    'detail' : detail,
                    'promotions' : promotions,
                }
            ]
        })
    
    # print(ls_json, len(ls_json))
    
    return ls_json

def get_model11(path):
    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th tH5 tH3 fDtacB">(.*)</div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'

    apple_base = DTAC_BASE + 'apple'
    page = requests.get(apple_base + path)
    page.encoding = 'utf-8'
    if page:
        print('Get page!!!')

    raw_data = re.findall(txt_raw, page.text)
    # print('len raw_data = ', len(raw_data)) # len = 8
    # print(raw_data[0])
    # data in 0
    # print('len raw_data[0] = ', len(raw_data[0]))

    ls_json = []

    for data in raw_data:
        model = None
        size = None
        detail = None
        contact = None
        promotions = []
        model = re.findall(txt_model, data[0])
        # print('model = ',model)
        if model != []:
            size = re.findall(txt_size, model[0])
            print(size)
        
        det = re.findall(txt_detail, data[0])
        if det == []:
            det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            if deta == []:
                deta = det[0][0]
            # print(deta)
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print('detail = ',detail)
            contact = re.findall(txt_contact, detail)
            if contact is None or contact == []:
                contact = '(สัญญา 24 เดือน)'
            # print(contact)
        
        tbody = re.findall(txt_tbody, data[0])
        # print(tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            print(price)
            promotions.append({
                'package_price': price[0],
                'advance_fee': price[1], 
                'dtac_price': price[2],
                'gold_price': None, 
                'platinum_price': None,
                })
            # print(promotions, len(promotions))

        ls_json.append({
            'model' : model[0],
            'size' : size[0],
            'package' : [
                {
                    'contact' : contact,
                    'detail' : detail,
                    'promotions' : promotions,
                }
            ]
        })
    
    print(ls_json, len(ls_json))
    
    return ls_json

def get_modelxr(path):
    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th txt-h-2 -bold">(.*)</div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'

    apple_base = DTAC_BASE + 'apple'
    page = requests.get(apple_base + path)
    page.encoding = 'utf-8'
    if page:
        print('Get page!!!')

    raw_data = re.findall(txt_raw, page.text)
    # print(raw_data)
    # print('len raw_data = ', len(raw_data)) # len = 8
    # print(raw_data[0])
    # # data in 0
    # print('len raw_data[0] = ', len(raw_data[0]))

    ls_json = []

    for data in raw_data:
        model = None
        size = None
        detail = None
        contact = None
        promotions = []
        model = re.findall(txt_model, data[0])
        # print('model = ',model)
        if model != []:
            size = re.findall(txt_size, model[0])
            # print(size)
        
        det = re.findall(txt_detail, data[0])
        if det == []:
            det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
        # print('det = ', det)
        if det != []:
            deta = re.findall(txt_det, det[0][0])
            if deta == []:
                deta = det[0][0]
            # print(deta)
            detail = ''
            for i in deta:
                detail += str(i.strip())
            # print('detail = ',detail)
            contact = re.findall(txt_contact, detail)
            if contact is None or contact == []:
                contact = '(สัญญา 24 เดือน)'
            # print(contact)
        
        tbody = re.findall(txt_tbody, data[0])
        # print('tbody = ', tbody)
        # print(len(tbody[0]))
        tr = re.findall(txt_tr, tbody[0][0])
        # print(tr, len(tr))
        for td in tr:
            price = re.findall(txt, td[0])
            # print(price)
            promotions.append({
                'package_price': price[0],
                'advance_fee': None, 
                'dtac_price': price[1],
                'gold_price': None, 
                'platinum_price': None,
                })
            # print(promotions, len(promotions))

        ls_json.append({
            'model' : model[0],
            'size' : size[0],
            'package' : [
                {
                    'contact' : contact,
                    'detail' : detail,
                    'promotions' : promotions,
                }
            ]
        })
        break # dont delete this line 
    
    # print(ls_json, len(ls_json))
    
    return ls_json

def apple(order):
    iphone13pro = '/iphone-13-pro'
    iphone13 = '/iphone-13'
    iphone12 = '/iphone-12.html'
    iphonese = '/iphone-se.html'
    iphone11 = '/iphone-11.html'
    iphonexr = '/iphone-xr.html'
    if order == 'all':
        json = []
        json += get_model13(iphone13pro)
        json += get_model13(iphone13)
        json += get_model12(iphone12)
        json += get_modelse(iphonese)
        json += get_model11(iphone11)
        json += get_modelxr(iphonexr)
        # print(json, len(json))
        return json
    elif order == 'iphone13pro':
        return get_model13(iphone13pro)
    elif order == 'iphone13':
        return get_model13(iphone13)
    elif order == 'iphone12':
        return get_model12(iphone12)
    elif order == 'iphonese':
        return get_modelse(iphonese)
    elif order == 'iphone11':
        return get_model11(iphone11)
    elif order == 'iphonexr':
        return get_modelxr(iphonexr)

# apple('all')

def samsung(order):
    s22 = 'samsung-galaxy-s22'
    s21 = 'samsung-galaxy-s21-fe'
    z = 'galaxy-z'
    
    txt_raw = r'class="table-responsive">((.|\n)*?)<\/table>'
    txt_model = r'<div class="txt-th txt-h-2 -bold">(.*)</div>'
    txt_tbody = r'<tbody class="table-package">((.|\n)*?)<\/tbody>'
    txt_tr = r'<tr>((.|\n)*?)<\/tr>'
    txt_detail = r'<div class="txt-th cWhite"((.|\n)*?)\/div>'
    txt_det = r'[^<>\n\t]+(?=[<\n])'
    txt_size = r'[0-9]+[G|T]B'
    txt_contact = r'\(.*\)'

    def get_model22(path):
        # s22 and z
        page = requests.get(DTAC_BASE + 'samsung/' + path)
        page.encoding = 'utf-8'
        print('Get page!!!') if page else print('Dont get page!!!')

        raw_data = re.findall(txt_raw, page.text)
        # print(raw_data)
        # print('len raw_data = ', len(raw_data)) # len = 8
        # print(raw_data[0])
        # # data in 0
        # print('len raw_data[0] = ', len(raw_data[0]))

        ls_json = []

        for data in raw_data:
            model = None
            size = None
            detail = None
            contact = None
            promotions = []
            model = re.findall(txt_model, data[0])
            # print('model = ',model)
            if model == []:
                model = re.findall(r'<div class="txt-th tH5 tH3 fDtacB">(.*)</div>', data[0])
            if model != []:
                size = re.findall(txt_size, model[0])
                # print(size)
            det = re.findall(txt_detail, data[0])
            if det == []:
                det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
            # print('det = ', det)
            if det != []:
                deta = re.findall(txt_det, det[0][0])
                if deta == []:
                    deta = det[0][0]
                # print(deta)
                detail = ''
                for i in deta:
                    detail += str(i.strip())
                # print('detail = ',detail)
                contact = re.findall(txt_contact, detail)
                if contact is None or contact == []:
                    contact = '(สัญญา 24 เดือน)'
                # print(contact)
            tbody = re.findall(txt_tbody, data[0])
            # print('tbody = ', tbody)
            # print(len(tbody[0]))
            tr = re.findall(txt_tr, tbody[0][0])
            # print(tr, len(tr))
            for td in tr:
                price = re.findall(txt, td[0])
                # print(price)
                promotions.append({
                    'package_price': price[0],
                    'advance_fee': price[1], 
                    'dtac_price': price[2],
                    'gold_price': price[3], 
                    'platinum_price': price[4],
                    })
                # print(promotions, len(promotions))

            ls_json.append({
                'model' : model[0],
                'size' : size[0],
                'package' : [
                    {
                        'contact' : contact,
                        'detail' : detail,
                        'promotions' : promotions,
                    }
                ]
            })

        if path == z:
            ls_json.pop(0)
            ls_json.pop(0)

        # print(ls_json, len(ls_json))
        
        return ls_json

    def get_model21():
        page = requests.get(DTAC_BASE + 'samsung/' + s21)
        page.encoding = 'utf-8'
        print('Get page!!!') if page else print('Dont get page!!!')

        raw_data = re.findall(txt_raw, page.text)
        # print(raw_data)
        # print('len raw_data = ', len(raw_data)) # len = 8
        # print(raw_data[0])
        # # data in 0
        # print('len raw_data[0] = ', len(raw_data[0]))

        ls_json = []

        for data in raw_data:
            model = None
            size = None
            detail = None
            contact = None
            promotions = []
            model = re.findall(txt_model, data[0])
            # print('model = ',model)
            if model == []:
                model = re.findall(r'<div class="txt-th tH5 tH3 fDtacB">(.*)</div>', data[0])
            if model != []:
                size = re.findall(txt_size, model[0])
                # print(size)
            det = re.findall(txt_detail, data[0])
            if det == []:
                det = re.findall(r'<div class="txt-th -c-white">((.|\n)*?)<\/div>', data[0])
            # print('det = ', det)
            if det != []:
                deta = re.findall(txt_det, det[0][0])
                if deta == []:
                    deta = det[0][0]
                # print(deta)
                detail = ''
                for i in deta:
                    detail += str(i.strip())
                # print('detail = ',detail)
                contact = re.findall(txt_contact, detail)
                if contact is None or contact == []:
                    contact = '(สัญญา 24 เดือน)'
                # print(contact)
            tbody = re.findall(txt_tbody, data[0])
            # print('tbody = ', tbody)
            # print(len(tbody[0]))
            tr = re.findall(txt_tr, tbody[0][0])
            # print(tr, len(tr))
            for td in tr:
                price = re.findall(txt, td[0])
                # print(price)
                promotions.append({
                    'package_price': price[0],
                    'advance_fee': price[1], 
                    'dtac_price': price[2],
                    'gold_price': price[3], 
                    'platinum_price': price[3],
                    })
                # print(promotions, len(promotions))

            ls_json.append({
                'model' : model[0],
                'size' : size[0],
                'package' : [
                    {
                        'contact' : contact,
                        'detail' : detail,
                        'promotions' : promotions,
                    }
                ]
            })

        
        print(ls_json, len(ls_json))
        
        return ls_json
    
    if order == 'all':
        json = get_model22(s22)
        json += get_model22(z)
        json += get_model21()
        return json
    elif order == 's22':
        return get_model22(s22)
    elif order == 's21':
        return get_model21()
    elif order == 'z':
        return get_model22(z)
    else:
        return 'no order'

# samsung()

def scraping(brand):
    txt_product = r'<div class="item-mobile product"((.|\n)*?)<ul class="txt-body-s">((.|\n)*?)<\/div>'
    txt_sprice = r'data-price="(.*)" '
    txt_name = r'data-name="(.*)"'
    txt_price = r'<u>(.*)?<\/u>'
    txt_detail = r'<li>(.*)?<\/li>'
    
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

# scraping('samsung')