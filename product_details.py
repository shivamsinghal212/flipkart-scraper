import logging
import re
import requests
from bs4 import BeautifulSoup as Bs

from product_classes import product_details_classes

logging.basicConfig(filename='logs', level=logging.DEBUG)

URL = [
    'https://www.flipkart.com/apple-iphone-se-black-64-gb/p/itm832dd5963a08d?pid=MOBFRFXHCKWDAC4A&lid=LSTMOBFRFXHCKWDAC4AEQROVZ&marketplace=FLIPKART&srno=b_1_1&otracker=nmenu_sub_Electronics_0_iPhone%20SE&fm=organic&iid=73ae50ec-7a1f-4ebe-b290-c283fb8e51ec.MOBFRFXHCKWDAC4A.SEARCH&ppt=browse&ppn=browse&ssid=4hd8tkgnwg0000001601412078132',
    'https://www.flipkart.com/barbie-kids-play-indoor-outdoor-tent-house/p/itmf2fdxk3ygsnth?pid=OTYF2FCEFRSGGT4T&lid=LSTOTYF2FCEFRSGGT4TOTDGBB&marketplace=FLIPKART&srno=b_1_2&otracker=nmenu_sub_Baby%20%26%20Kids_0_Outdoor%20Toys&fm=organic&iid=ca6808c0-661f-4cea-bb47-98712cd7814f.OTYF2FCEFRSGGT4T.SEARCH&ppt=browse&ppn=browse&ssid=405lyqu8tc0000001601414478215'
]


class TextUtilities:
    @staticmethod
    def format_price(text):
        digit_lis = re.findall(r'\d+', text)
        data = ''.join(digit_lis)
        return float(data)


class ProductScrapper:

    def __init__(self, url):
        self.url = url
        self.name = None
        self.price = None
        self.orig_price = None
        self.rating = None

    def initialize(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self._scrape_raw_product_details(response)
            print(self.name)
            print(self.price)
            print(self.orig_price)
            print(self.rating)
            return True
        else:
            logging.error(response.status_code)
            print('Request timed out, Poor connection.Try again.')

    def _scrape_raw_product_details(self, response):
        raw_html = response.content
        soup = Bs(raw_html, 'html.parser')
        self._set_name(soup)
        self._set_price(soup)
        self._set_original_price(soup)
        self._set_rating(soup)

    def _set_name(self, soup: Bs):
        name_class = product_details_classes['name']
        data = soup.find(name_class['tag'], {'class': name_class['value']})
        if data:
            self.name = data.get_text()

    def _set_price(self, soup: Bs):
        name_class = product_details_classes['price']
        data = soup.find(name_class['tag'], {'class': name_class['value']})
        if data:
            self.price = TextUtilities().format_price(data.get_text())

    def _set_original_price(self, soup: Bs):
        name_class = product_details_classes['orig_price']
        data = soup.find(name_class['tag'], {'class': name_class['value']})
        if data:
            self.orig_price = TextUtilities().format_price(data.get_text())

    def _set_rating(self, soup: Bs):
        name_class = product_details_classes['rating']
        data = soup.find(name_class['tag'], {'class': name_class['value']})
        if data:
            self.rating = data.get_text()


if __name__ == '__main__':
    print('Enter URL of item:')
    search = URL[0]
    ProductScrapper(url=search).initialize()
