
import requests
import re
import json

# TRUE = "https://store.truecorp.co.th/online-store/item/L91759660?ln=th&_ga=2.96047327.2117052161.1647572364-1913214076.1647421330&matcode=3000093932&selected_campaign=mnp_bundling_existing&rc=1699"
# TRUE_PACKAGE = 'https://truemoveh.truecorp.co.th/package/postpaid'
# AIS = 'https://www.hotdeal.ais.co.th/hotdeal-samsung.html'
AIS_APPLE = 'https://www.hotdeal.ais.co.th/hotdeal-apple.html'
TRUE_APPLE = 'https://store.truecorp.co.th/online-store/item/L91759660?ln=th&_ga=2.156839603.946800142.1648195462-1913214076.1647421330&matcode=3000093932&selected_campaign=mnp_bundling_existing&rc=1699'
# url = AIS

page = requests.get(AIS_APPLE)
page.encoding = 'utf-8'
print('After requests')
# print(page.encoding)
# print(page.text)

x = [{
    'model': 'iPhone 13 Pro Max',
    'size' : '1 TB',
    'type' : 'รายเดือน',
    'details' : 'pack 699 ลดเพิ่ม 1000',
    'normalprice' : 62900,
    'promotions' : [
        {
            'specialprice' : 58900,
            'paid' : 2000,
            'package' : 699,
        },
        {
            'specialprice' : 55900,
            'paid' : 3000,
            'package' : 1199,
        },
        {
            'specialprice' : 54400,
            'paid' : 4000,
            'package' : 1499,
        }
    ]
}]

x[0].update({'name' : 'nut'})
x_json = json.dumps(x, ensure_ascii=False)

print(type(x_json))

a = json.loads(x_json)

print(type(a))
print(a)
for i in a:
    promotions = i.get('promotions')
    print(promotions)
    for j in promotions:
        print(j)


d = [1, 2, 3, 4]
print(d[-2])