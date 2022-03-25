# import regex.ais as scrap
# from regex import test_bs4 as test
import json
# x = scrap.get_iphone_5g()
# print(type(x))
# # test.Hello()

x = ['ฟหก', '่าสว', 'ผปแ']
y = json.dumps(x, ensure_ascii=False)
print(y)