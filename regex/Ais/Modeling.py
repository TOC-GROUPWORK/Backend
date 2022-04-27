import ais 
import json
import requests
import ast

raw_data = ais.get_iphone(1)
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
                    'name': item['model'].strip(),
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
            'provider': 'AIS'
        }

        provider_res = requests.post('http://127.0.0.1:8000/provider', json = provider_data)
        provider_res = provider_res._content.decode('utf-8')
        provider_res = ast.literal_eval(provider_res)

        ram = ''.join(item['size'].split(' '))
        print(ram)
        data_detail = { 'provider_id': provider_res['_id'], 'ram': ram }
        detail_response = requests.post('http://127.0.0.1:8000/detail', json = data_detail)
        detail_response = detail_response._content.decode('utf-8')
        detail_response = json.loads(ast.literal_eval(repr(detail_response)))

        promotion_dict = dict()

        name = str(item['detail']) 

        for promotion in item['promotions']:

            price = promotion['specialprice']
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
            sprice = promotion['specialprice']
            prepaid_price = promotion['paid']
            package_price = promotion['package']
            package_type = '12'
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