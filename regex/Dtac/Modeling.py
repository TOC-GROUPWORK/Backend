import dtac
import json
import requests
import ast
import re

iphone13pro = '/iphone-13-pro'
iphone13 = '/iphone-13' 
iphone12 = '/iphone-12.html' # pass
iphonese = '/iphone-se.html' # pass
iphone11 = '/iphone-11.html' # pass
iphonexr = '/iphone-xr.html' # pass
apple = 'apple/'
samsung = 'samsung/'
s22 = 'samsung-galaxy-s22'
s21 = 'samsung-galaxy-s21-fe'
z = 'galaxy-z'

raw_data = dtac.apple('iphone13')
# data = raw_data[0]
with open('test.json', 'w', encoding='utf-8') as writefile:
    json.dump(raw_data, writefile, ensure_ascii=False)
print('Done writing .json')

def get_brands() -> list[str]:
    print('GET ALL BRANDS!!')
    response = requests.get('http://127.0.0.1:8000/brands')
    response = response._content.decode('utf-8')
    response = ast.literal_eval(response)

    return response

def main():
    print('START GET DATA')
    brands = get_brands()
    # with open('brands.json', 'w', encoding='utf-8') as writefile:
    #     json.dump(brands, writefile, ensure_ascii=False)
    # print('Done writing .json')
    # print(brands)
    brand_id = None
    for brand in brands:
        if "Apple" == brand["name"]:
            brand_id = brand["_id"]
            break
    # print(brand_id)

    for item in raw_data:
        print()
        print('item = ',item)
        product = {
                    'brand_id': brand_id,
                    'name': item['model'][0],
                    'color_name' : [],
                    'link_ais' : 'string',
                    'link_true' : 'string',
                    'link_dtac' : 'string',
                    'color_style' : [],
                    'img': [],
                }
        # print(product)
        response = requests.post('http://127.0.0.1:8000/model', json = product)
        response = response._content.decode('utf-8')
        response = ast.literal_eval(response)
        # print(response['_id'])
        # requests.put(f'http://127.0.0.1:8000/model/{response["_id"]}', json = {"link_dtac" :  })
        print(response)
        provider_data = {
            'model_id': response['_id'],
            'provider': 'DTAC'
        }

        provider_res = requests.post('http://127.0.0.1:8000/provider', json = provider_data)
        provider_res = provider_res._content.decode('utf-8')
        provider_res = ast.literal_eval(provider_res)

        ram = item['size'][0]
        data_detail = { 'provider_id': provider_res['_id'], 'ram': ram }
        detail_response = requests.post('http://127.0.0.1:8000/detail', json = data_detail)
        detail_response = detail_response._content.decode('utf-8')
        detail_response = json.loads(ast.literal_eval(repr(detail_response)))

        for package in item['package']:
            print('package = ', package)
            promotion_dict = dict()

            name = str(package['detail']) 

            for promotion in package['promotions']:

                price = promotion['dtac_price']
                # print(name, price)

                promotion_dict['model_detail_id'] = detail_response['_id']
                promotion_dict['name'] = name
                promotion_dict['detail'] = f'เริ่มต้น {price} บาท'
                # print()
                # print(promotion_dict)
                promotion_res = requests.post('http://127.0.0.1:8000/promotion', json = promotion_dict)
                promotion_res = promotion_res._content.decode('utf-8')
                promotion_res = json.loads(ast.literal_eval(repr(promotion_res)))

                # print(promotion_res)
                # print(promotion)
                sprice = promotion['dtac_price']
                prepaid_price = promotion['advance_fee']
                package_price = promotion['package_price']
                contact = re.findall(r'[0-9]+', package['contact'])
                if contact == []:
                    contact = ['12']
                print(contact)
                package_type = contact[0]
                detail = '-'

                p_data = {
                            'package_no' : None,
                            'promotion_id' : promotion_res['_id'],
                            'specialprice' : sprice,
                            'prepaid' : str(prepaid_price),
                            'package' : package_price,
                            'package_type' : package_type,
                            'package_detail': detail,
                        }

                requests.post('http://127.0.0.1:8000/package', json = p_data)

main()