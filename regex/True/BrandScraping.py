import re
import ast
import requests
import asyncio
from pyppeteer import launch
import os

MAIN_TRUE = 'https://truemoveh.truecorp.co.th/device#'

# MAIN PAGE FOR BRANDS SCRAPING
# '<div class="opt-list " data-name="select_brand" data-id="[\d]*".+</div>'
BRAND_LIST = r'<div [a-eilm-pr-t="\-_ ]+ [adit"=\-]*[\d]+["]+? .+<\/div>'                     
                         
# <span class="opt-txt">Apple</span>
BRAND_NAME = r'<span [aclopstx="->]+(.+)<\/span>'

# BRAND PAGE FOR MODELS SCRAPING
# '<span class="hpl-red-txt">[0-9]*</span>'
PAGE_QUANTITY = r'<span [acdehlprstx"=\- ]*>([\d]*)<\/span>'

# MODEL GRID BOX
# GET MODEL LIST
# '<ul id="grid-box" class="box-inner-list-cl clearfix">((.|\n)+?)</ul>'
GRID_BOX = r'<ul i[a-gilnorstx="\- ]+?>((.|\n)+?)<\/ul>'

# GET MODEL
# '<li class="filter-items" .*>((.|\n)+?)</li>'
GRID_FILTER = r'<li [acefilmrst="-]+ .*>((.|\n)+?)<\/li>'

# MODEL_LINK
# '<a href="https://store.truecorp.co.th/online-store/item/[A-Z0-9]+?\?ln=th">'
MODEL_LINK = r'<a href="([a-zA-Z0-9-=\/?.:]+?)">'

# MODEL_NAME
# ' class="txt-brand">iPhone 13 Pro Max</a>'
MODEL_NAME = r' [a-dlnrstx="-]+>(.+?)<\/a>'

def get_brands(main_url: str) -> list[str]:
     print('GET ALL BRANDS!!!')
     page = requests.get(main_url)
     page.encoding = 'utf-8'

     # print(page.text)
     brands_list = re.findall(BRAND_LIST, page.text)

     brands = []
     for brand in brands_list:

          brand_name = re.findall(BRAND_NAME, brand)[0]
          print(brand_name)

          data = { 'name': brand_name, }
          response = requests.post('http://127.0.0.1:8000/brand', json = data)
          response = response._content.decode('utf-8')
          response = ast.literal_eval(response)
          # print(repr(response))
          brands.append(response)

     # f= open(f"page.txt","w+", encoding="utf-8")
     # f.write(page.text)
     # f.close()

     return brands

async def get_page_quantity(page, brand: str) -> int:
     print('\nGET MODELS AT ' + str.upper(brand) + ' brand!!!')
     uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=1'
     # print(uri)

     await page.goto(uri)
     await page.waitFor(1000)
     # GET BODY HTML
     page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')

     page_quantity = re.findall(PAGE_QUANTITY, page_body)[0]
     print(page_quantity)

     # await page.close()
     return int(page_quantity)

async def get_models_at_page(page, brand: str, page_no: int) -> list[str]:
     print('PAGE %d' % page_no)

     uri = 'https://truemoveh.truecorp.co.th/device?search_brand=' + brand + '&search_network=all&page=' + str(page_no)
     print(uri)

     try:
          await page.goto(uri)
          await page.waitFor(2000)
     except:
          return []

     # GET BODY HTML
     page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')
     f= open(f"page.txt","w+", encoding="utf-8")
     f.write(page_body)
     f.close()

     # <ul id="grid-box" class="box-inner-list-cl clearfix">
     grid_box = re.findall(GRID_BOX, page_body)[0][0]
     # print(grid_box)
     model_list = re.findall(GRID_FILTER, grid_box)

     links = []
     for model in model_list:
          model = model[0]
          # print(model)
          try:
               link = re.findall(MODEL_LINK, model)[0]
               name = re.findall(MODEL_NAME, model)[0].strip()
          except:
               continue
          links.append(link)
          print(link)
          print(name)

     # print(grid_box)
     print()
     return links

async def get_models(page, brand: str, id: str, page_quantity: int):

     print('GET ALL MODELS')

     model_links = []
     for page_no in range(page_quantity):
          model_links += await get_models_at_page(page, brand, page_no + 1)
          break
     if len(model_links) == 0:
          return
     # f = open(f'files/{brand}.txt', 'r')
     # for link in f:
     #      model_links.append(link.split('\n')[0])
     # f.close()

     data = { 'true': model_links }
     response = requests.put('http://127.0.0.1:8000/brand/' + id, json = data)
     # response = response._content.decode('utf-8')
     # response = ast.literal_eval(response)
     # print(repr(response))
     # f= open(f"files/{brand}.txt","w")
     # f.write('\n'.join(model_links))
     # f.close()
     return

async def main():
     print("Start TRUE Scraping!!!!")

     db = dict()
     brands = get_brands(MAIN_TRUE)
     
     browser = await launch()
     page = await browser.newPage()
     await page.setViewport({'width': 1920, 'height': 1080})

     for brand in brands:
          # response = requests.get('http://127.0.0.1:8000/brand/' + brand['_id'])
          # response = response._content.decode('utf-8')
          # response = ast.literal_eval(response)
          # if response['true'] != []:
          #      continue
          # print(response['true'])
          page_quantity: int = await get_page_quantity(page, brand['name'])
          await get_models(page, brand['name'], brand['_id'], page_quantity)

     await page.close()

asyncio.get_event_loop().run_until_complete(main())