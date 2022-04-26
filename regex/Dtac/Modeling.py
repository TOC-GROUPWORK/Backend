import dtac
import json
import requests
import ast

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

data = dtac.samsung()
with open('test.json', 'w', encoding='utf-8') as writefile:
    json.dump(data, writefile, ensure_ascii=False)
print('Done writing .json')

def get_brands() -> list[str]:
    print('GET ALL BRANDS!!')
    response = requests.get('http://127.0.0.1:8000/brands')
    response = response._content.decode('utf-8')
    response = ast.literal_eval(response)

    return response


# print('START GET DATA')
# brands = get_brands()
# with open('brands.json', 'w', encoding='utf-8') as writefile:
#     json.dump(brands, writefile, ensure_ascii=False)
# print('Done writing .json')
# print(brands)

# product = {
#             'brand_id': id,
#             'name': data.model,
#             'color_name' : None,
#             'color_style' : None,
#             'img': None,
#         }

# response = requests.post('http://127.0.0.1:8000/model', json = product)
# response = response._content.decode('utf-8')
# response = ast.literal_eval(response)
# # print(response['_id'])

# provider_data = {
#     'model_id': response['_id'],
#     'link' : None,
#     'provider': 'DTAC'
# }

# provider_res = requests.post('http://127.0.0.1:8000/provider', json = provider_data)
# provider_res = provider_res._content.decode('utf-8')
# provider_res = ast.literal_eval(provider_res)

# data = { 'provider_id': provider_res['_id'], 'ram': data.size }
# detail_response = requests.post('http://127.0.0.1:8000/detail', json = data)
# detail_response = detail_response._content.decode('utf-8')
# detail_response = json.loads(ast.literal_eval(repr(detail_response)))

# promotion_dict = dict()

# name = None
# price = re.findall(START_PRICE, promotion[0])[0]
# print(name, price)

# promotion_dict['model_detail_id'] = detail_response['_id']
# promotion_dict['name'] = name
# promotion_dict['detail'] = f'เริ่มต้น {price} บาท'

# if promotion_dict['name'] == 'เครื่องเปล่า':
#     data = { 'normalprice': promotion_dict['detail'] }
#     requests.put('http://127.0.0.1:8000/detail/' + detail_response['_id'], json = data)
#     continue

# promotion_res = requests.post('http://127.0.0.1:8000/promotion', json = promotion_dict)
# promotion_res = promotion_res._content.decode('utf-8')
# promotion_res = json.loads(ast.literal_eval(repr(promotion_res)))

# p_data = {
#             'package_no' : None,
#             'promotion_id' : promotion_res['_id'],
#             'specialprice' : price,
#             'prepaid' : prepaid_price[0] if len(prepaid_price) > 0 else '-',
#             'package' : package_price,
#             'package_type' : package_type,
#             'package_detail': detail,
#         }

# requests.post('http://127.0.0.1:8000/package', json = p_data)