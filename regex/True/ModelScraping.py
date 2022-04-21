import re
import ast
import asyncio
import requests
from pyppeteer import launch
import json

STORE_DETAIL        = r'<div class="page online-store-detail">((.|\n)+?)</script></div></div></div>'
IMAGE_CONTAINER     = r'<div class="stickyProb">((.|\n)+?)<div class="grid gap-4 lg:gap-8 mb-auto">'
DETAIL_CONTAINER    = r'<div class="grid gap-4 lg:gap-8 mb-auto">((.|\n)+?)</div></div></div></div></div>'

PRODUCT_IMAGE       = r'<img data-v-2f2705a3="" src="((.)+?)" alt="Product Image" class="carousel">'
NAME_CONTAINER      = r'(<div class="grid gap-4" id="device-price-id">((.|\n)+?)[!<>-]*</div></div>)'
PRODUCT_NAME        = r'<div class="flex justify-between"><div class="[a-z0-9 -]*">((.)+?)</div></div>'

COLOR_NAME          = r'<label class="w-full break-word" style="opacity: [0-9.]+?;">[ \n]+?[ ]+([a-zA-Z ]+?)[ \n]+?</label>'
COLOR_STYLE         = r'<div class=\"[a-z0-9- [\]]* shadow-inset\" ((.)+)></div></button>'
COLOR_BG            = r'style=\"[background\-clo]+: rgb[(]([0-9]+?), ([0-9]+?), ([0-9]+?)[)];\"'

RAM_LIST            = r'<button data-options-.+?-id="[0-9]+?" class="[a-z0-9 :-]+?">([a-zA-Z0-9]+?)</button>'
# RAM_LIST            = r'<button [disable=" ]*?data-options-.+?-id="[0-9]+?" class="[a-z0-9 :-]+?">([a-zA-Z0-9]+?)</button>'

PROMOTION_CONTAINER = r'(<div class="flex-auto">(.|\n)+?)<div class="accordion flex flex-col items-end is-closed">'
PROMOTION_BOX       = r'(<button [adtespromin-]+?="[a-z0-9_]+?" [clas]+?="[a-z :-]+?" style="[a-z0-9 :;]+?">((.|\n)+?)</button>)'
PACKAGE_BOX         = r'(<button ([adtespckgi-]+?="[a-z0-9_]+?"| |[clas]+?="[a-z :-]+?" style="[a-z0-9 :;]+?")+?>((.|\n)+?)</button>)'

PROMOTION_NAME      = r'<div class="flex-1 text-center font-medium" style="font-size: 20px;">[ \n]+?[ ]+(.+)[ \n]+?</div>'
START_PRICE         = r'<div class="text-red text-3xl font-bold">([0-9,]+)+?[.-]+</div>'

PACKAGE_NEW_USER    = r"<div class=\"flex flex-col grid h-full text-20 font-light cursor-pointer\" style=\"min-width: 192px;\">((.|\n)+?</path></svg></div></div>)</div>"

PROMOTION_PRICE     = r'<div class="text-44">[ ]?([0-9,]+)+?[.-]+</div>|<div class=\"[texcnrxldfobp 23\-]+\">[ \n]+([0-9,]+)+?[.-]+[ \n]+</div>' # r'<div class="text-44">[ ]?([0-9,.-]+)</div>'
PACKAGE_PRICE       = r'<span class=\"font-bold text-22\">[ \n]*([0-9,]+)+?[.-]+</span>[\n]'
PREPAID_PRICE       = r'<span class="font-bold text-22">[ \n]*([0-9,]+)+?[.-]+</span></div>'
PACKAGE_TYPE        = r'<span class=\"font-bold text-22\">[ \n]+([0-9]+)+?[ \n]+.+[ \n]+</span>'

PACKAGE_DETAIL      = r'<div class=\"grid place-items-center bg-red-pink-gradient text-white text-xl p-4 py-2 mw-[\[]350px[\]] h-[\[]100px[\]]\"><!---->[\ \n]+?[\ ]+(.+)[\n][\ ]+?</div>'

def get_brands() -> list[str]:
    print('GET ALL BRANDS!!')
    response = requests.get('http://127.0.0.1:8000/brands')
    response = response._content.decode('utf-8')
    response = ast.literal_eval(response)

    return response

async def get_promotions(page, provider_id: str, rams: list[str]) -> dict:

    for index, ram in enumerate(rams):

        print(ram)

        selector = f'div.grid.lg\:grid-col-\[80px-1fr\].gap-4.lg\:gap-4 > div:nth-child(4) > div:nth-child({index + 1}) > button.p-4.py-2'
        # print(selector)
        try:
            await page.click(selector)
            await page.waitFor(5000)
            # await page.screenshot({'path': f'{ram}.png'})
        except:
            if ram != "page":
                continue
            pass

        data = { 'provider_id': provider_id, 'ram': ram }
        detail_response = requests.post('http://127.0.0.1:8000/detail', json = data)
        detail_response = detail_response._content.decode('utf-8')
        detail_response = json.loads(ast.literal_eval(repr(detail_response)))
        # print(detail_response)

        page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')

        promotion_container = re.findall(PROMOTION_CONTAINER, page_body)[0][0]
        promotion_box = re.findall(PROMOTION_BOX, promotion_container)

        # promotions = await page.querySelectorAll('div.flex-auto > div > div.grid.gap-1.grid-flow-col > button.rounded-xl.w-full.hover\:shadow-lg')

        for index, promotion in enumerate(promotion_box):
            print("Promotion" if index == 0 else "", end=" ")

            promotion_dict = dict()

            name = re.findall(PROMOTION_NAME, promotion[0])[0]
            price = re.findall(START_PRICE, promotion[0])[0]
            print(name, price)

            promotion_dict['model_detail_id'] = detail_response['_id']
            promotion_dict['name'] = name
            promotion_dict['detail'] = f'เริ่มต้น {price} บาท'

            if promotion_dict['name'] == 'เครื่องเปล่า':
                data = { 'normalprice': promotion_dict['detail'] }
                requests.put('http://127.0.0.1:8000/detail/' + detail_response['_id'], json = data)
                continue

            promotion_res = requests.post('http://127.0.0.1:8000/promotion', json = promotion_dict)
            promotion_res = promotion_res._content.decode('utf-8')
            promotion_res = json.loads(ast.literal_eval(repr(promotion_res)))
            # print(type(promotion_res))

            selector = f'div.flex-auto > div > div.grid.gap-1.grid-flow-col > button.rounded-xl.w-full.hover\:shadow-lg:nth-child({index + 1}) > div'
            # print(selector)
            
            await page.click(selector, { 'delay': 3,})
            # await promotions[index].click()
            await page.waitFor(1000)
            # await page.screenshot({'path': f'{index}.png', 'fullPage': True})

            page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')

            promotion_container = re.findall(PROMOTION_CONTAINER, page_body)[0][0]

            package_box = re.findall(PACKAGE_BOX, promotion_container)
            # print(len(package_box))

            promotion_dict['package'] = list()
            for index, package in enumerate(package_box):
                # print(package[0]) 
                print("Package" if index == 0 else "", end="")

                detail = "EMPTY TEXT"
                if name == "ลูกค้าปัจจุบันทรูมูฟ เอช":
                    detail = re.findall(PACKAGE_DETAIL, package[0])[0]
                    packages = re.findall(PACKAGE_NEW_USER, package[0])
                    for i, p in enumerate(packages):
                        price = re.findall(PROMOTION_PRICE, p[0])[0][1]
                        package_price = re.findall(PACKAGE_PRICE, p[0])[0]
                        prepaid_price = re.findall(PREPAID_PRICE, p[0])
                        package_type = re.findall(PACKAGE_TYPE, p[0])[0]

                        p_data = {
                            'package_no' : str(index) + str(i),
                            'promotion_id' : promotion_res['_id'],
                            'specialprice' : price,
                            'prepaid' : prepaid_price[0] if len(prepaid_price) > 0 else '-',
                            'package' : package_price,
                            'package_type' : package_type,
                            'package_detail': detail,
                        }

                        requests.post('http://127.0.0.1:8000/package', json = p_data)
                else:
                    price = re.findall(PROMOTION_PRICE, package[0])[0][0]
                    package_price = re.findall(PACKAGE_PRICE, package[0])[0]
                    prepaid_price = re.findall(PREPAID_PRICE, package[0])
                    package_type = re.findall(PACKAGE_TYPE, package[0])[0]

                    p_data = {
                        'package_no' : str(index),
                        'promotion_id' : promotion_res['_id'],
                        'specialprice' : price,
                        'prepaid' : prepaid_price[0] if len(prepaid_price) > 0 else '-',
                        'package' : package_price,
                        'package_type' : package_type,
                    }

                    requests.post('http://127.0.0.1:8000/package', json = p_data)
        print()


async def get_model_data(page, id: str, link: str):
    try:
        await page.goto(link)
        await page.waitFor(5000)
        # await page.screenshot({ 'path': 'image.png'})

        page_body = await page.evaluate('() => document.getElementsByTagName("BODY")[0].innerHTML')
        container = re.findall(STORE_DETAIL, page_body)[0][0]

        # GET PRODUCT IMAGE
        image_container = re.findall(IMAGE_CONTAINER, container)[0][0]
        product_image = [link[0] for link in re.findall(PRODUCT_IMAGE, image_container)]

        # GET PRODUCT DETAIL AND PROMOTION
        detail_container = re.findall(DETAIL_CONTAINER, container)[0][0]

        # GET PRODUCT NAME
        name_container = re.findall(NAME_CONTAINER, detail_container)[0][0]
        product_name = re.findall(PRODUCT_NAME, name_container)[0][0]
        print(product_name)

        # GET PRODUCT COLOR
        color_name = [name.strip() for name in re.findall(COLOR_NAME, detail_container)]
        color_style = [style[0] for style in re.findall(COLOR_STYLE, detail_container)]

        background_color = list()
        for color in color_style:
            bg = re.findall(COLOR_BG, color)
            bg = [('255', '255', '255')] if not bg else bg
            background_color.append(bg[0])

        product = {
            'brand_id': id,
            'name': product_name,
            'color_name' : color_name,
            'color_style' : background_color,
            'img': product_image,
        }

        response = requests.post('http://127.0.0.1:8000/model', json = product)
        response = response._content.decode('utf-8')
        response = ast.literal_eval(response)
        # print(response['_id'])

        provider_data = {
            'model_id': response['_id'],
            'link' : link,
            'provider': 'TRUE'
        }

        provider_res = requests.post('http://127.0.0.1:8000/provider', json = provider_data)
        provider_res = provider_res._content.decode('utf-8')
        provider_res = ast.literal_eval(provider_res)

        # color = {
        #     'color_name' : color_name,
        #     'color_style' : background_color,
        # }

        # response = requests.put('http://127.0.0.1:8000/model/' + response['_id'], json = color)

        rams = re.findall(RAM_LIST, detail_container)
        ram_list = rams if len(rams) > 0 else ["page"]

        await get_promotions(page, provider_res['_id'], ram_list)

    except Exception as e:
        print(e)
        pass

    return None

async def get_model_iterator(page, brand: dict):
    for id, link in enumerate(brand['true']):
        await get_model_data(page, brand['_id'], link)

async def get_data(page, brands: list[str]):

    datas = dict()
    for brand in brands:
        await get_model_iterator(page, brand)

async def main():
    
    print('START GET DATA')
    brands = get_brands()

    browser = await launch(
        ignoreHTTPSErrors=True,
        headless=True,
        executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        # executablePath=os.getenv('CHROME_PATH'),
        args=[
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--headless',
        '--disable-gpu',
        '--ignore-certificate-errors'
        ]
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})

    await get_data(page, brands)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())