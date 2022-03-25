from bs4 import BeautifulSoup
import requests
import json

# https://www.true.th/truemoveh/postpaid/

URL = 'https://truemoveh.truecorp.co.th/package/postpaid'


def update(dicts, key, lists):
    if dicts == []:
        for list in lists:
            dicts.append({key: list})
    else:
        for dict, list in zip(dicts, lists):
            dict.update({key: list})

print('Hello bs4')
data = requests.get(URL)
soup = BeautifulSoup(data.text, features="html.parser")
# print(soup)
pak = soup.find_all('div',{'class':'list-section'})
# print(pak[0], len(pak))
# price = pak.find('span',{'class':'cost-package'})
# print(price)
# print('price : ', price.text)
prices = []
names = []
details = []
internets = []
mores = []
for datas in pak:
    price = datas.find('span', {'class':'cost-package'})
    # print(price.find('strong').text.split('บาท'))
    prices.append(int(price.find('strong').text.split('บาท')[0]))

    name = datas.find('span', {'class':'sg-txt'})
    names.append(name.text)

    call = datas.find('span', {'class':'group-txt-1'})
    # print(call)
    details.append(call.text.split('\n')[1].replace('\r', ''))

    internet = datas.find('span', {'class':'desc-speed'})
    internets.append(internet.text)
    
    link = datas.find(href=True)
    # print('https:'+link['href'].strip())
    mores.append('https:'+link['href'].strip())

sh = mores
# print(sh, len(sh))
# [{'country': country, 'wins': wins} for country, wins in zip(a, b)]
# jls = [{'name': name, 'price': price, 'detail': detail} for name, price, detail in zip(names, prices, details)]
# json list
jls = []
# for data, internet in zip(jls, internets):
#     data.update({'internet': internet})
update(jls, 'name', names)
update(jls, 'price', prices)
update(jls, 'detail', details)
update(jls, 'internet', internets)
update(jls, 'information', mores)

# print('jls : ', jls)

jsonString = json.dumps(jls)

# print(type(jsonString))
# print(jls)
for i in jls:
    print(i.get('name'), i.get('price'), i.get('detail'), i.get('internet'), i.get('information'))

