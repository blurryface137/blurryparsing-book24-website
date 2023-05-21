import scrapy
import re


class Book_scrapy(scrapy.Spider):
    name = 'book24'

    url = ['https://book24.ru/catalog/voennye-boeviki-4748/page-',
           'https://book24.ru/catalog/zarubezhnye-boeviki-2263/page-',
           'https://book24.ru/catalog/kriminalnye-boeviki-2261/page-',
           'https://book24.ru/catalog/otechestvennye-boeviki-2262/page-',
           'https://book24.ru/catalog/trilleri-1717/page-',
           'https://book24.ru/catalog/zarubezhnye-detektivy-2045/page-',
           'https://book24.ru/catalog/ironicheskiy-detektiv-1699/page-',
           'https://book24.ru/catalog/istoricheskie-detektivy-2046/page-',
           'https://book24.ru/catalog/klassicheskiy-detektiv-1698/page-',
           'https://book24.ru/catalog/politicheskiy-detektiv-1702/page-',
           'https://book24.ru/catalog/kriminalnyy-detektiv-1700/page-',
           'https://book24.ru/catalog/otechestvennye-detektivy-2071/page-',
           'https://book24.ru/catalog/sovremennyy-detektiv-1703/page-',
           'https://book24.ru/catalog/shpionskie-detektivy-2047/page-',
           'https://book24.ru/catalog/zarubezhnaya-dramaturgiya-3219/page-',
           'https://book24.ru/catalog/otechestvennaya-dramaturgiya-3226/page-',
           'https://book24.ru/catalog/klassicheskaya-poeziya-1718/page-',
           'https://book24.ru/catalog/sborniki-poezii-avtorov-raznykh-stran-1632/page-',
           'https://book24.ru/catalog/sovremennaya-poeziya-1719/page-',
           'https://book24.ru/catalog/sentimentalnaya-zarubezhnaya-proza-2270/page-',
           'https://book24.ru/catalog/intellektualnaya-proza-4747/page-',
           'https://book24.ru/catalog/istoricheskaya-proza-1705/page-',
           'https://book24.ru/catalog/klassicheskaya-zarubezhnaya-proza-2268/page-',
           'https://book24.ru/catalog/klassicheskaya-otechestvennaya-proza-2269/page-',
           'https://book24.ru/catalog/sentimentalnaya-otechestvennaya-proza-2271/page-',
           'https://book24.ru/catalog/sovremennaya-zarubezhnaya-proza-2272/page-',
           'https://book24.ru/catalog/sovremennaya-otechestvennaya-proza-2273/page-',
           'https://book24.ru/catalog/ezotericheskie-khudozhestvennye-knigi-1664/page-',
           'https://book24.ru/catalog/uzhasy-i-mistika-2054/page-',
           'https://book24.ru/catalog/alternativnaya-istoriya--1892/page-',
           'https://book24.ru/catalog/antiutopiya-4744/page-',
           'https://book24.ru/catalog/boevaya-fantastika-2053/page-',
           'https://book24.ru/catalog/geroicheskaya-fantastika-2060/page-',
           'https://book24.ru/catalog/detektivnaya-fantastika-2059/page-',
           'https://book24.ru/catalog/zarubezhnaya-fantastika--2050/page-',
           'https://book24.ru/catalog/istoricheskaya-fantastika-2061/page-',
           'https://book24.ru/catalog/kosmicheskaya-fantastika-2057/page-',
           'https://book24.ru/catalog/nauchnaya-fantastika-2051/page-',
           'https://book24.ru/catalog/boevoe-fentezi-2055/page-',
           'https://book24.ru/catalog/istoricheskoe-fentezi--2070/page-',
           'https://book24.ru/catalog/yumoristicheskaya-proza-3688/page-']

    def start_requests(self):
        for link in self.url:
            for i in range(1, 31):
                new_link = link + str(i)
                yield scrapy.Request(new_link, self.parse_books, headers={
                    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})

    def parse_books(self, response):
        urls = response.css('div.product-card__image-holder a::attr(href)').getall()
        for i in range(len(urls)):
            urls[i] = 'https://book24.ru' + urls[i]
        for page in urls:
            yield scrapy.Request(page, self.parse_book, headers={
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})

    def parse_book(self, response):
        price = response.css('meta[itemprop="price"]::attr(content)').get()
        genres = response.css('a.product-characteristic-link::text').getall()[2]
        pages = response.css('dd.product-characteristic__value::text').getall()[2].strip()
        if price and genres != 'Эксмо' and genres != 'АСТ' and genres != 'Центрполиграф' and pages != '2018' and pages != '2019' and pages != '2020' and pages != '2021' and pages != '2022' and pages != '2023' and 'мм' not in pages and '+' not in pages:
            return {
                'book_url': response.request.url,
                'name': response.css('h1.product-detail-page__title::text').get().split(':')[1].strip(),
                'author': response.css('h1.product-detail-page__title::text').get().split(':')[0].strip(),
                'genres': response.css('a.product-characteristic-link::text').getall()[2],
                'score': response.css('span.rating-widget__main-text::text').get().strip(),
                'pages': response.css('dd.product-characteristic__value::text').getall()[2].strip(),
                'price': response.css('meta[itemprop="price"]::attr(content)').get(),
                'description': response.css('.product-about__text p::text').get(),
                'cover link': response.css('.product-poster__main-image::attr(src)').get(),
                'reviews': response.css('div.review-item__review::text').getall()
            }
