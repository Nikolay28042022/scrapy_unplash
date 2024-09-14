import scrapy
from ..items import ImageItem

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_spider"
    start_urls = ['https://unsplash.com/t']  # Страница с категориями

    def parse(self, response):
        # Сбор ссылок на категории
        category_links = response.xpath('//a[@class="wuIW2 R6ToQ"]/@href').getall()

        for link in category_links:
            yield response.follow(link, self.parse_category)

    def parse_category(self, response):
        # Сбор ссылок на страницы с фотографиями
        category = response.xpath('//h1[@class="zbHmu L8kCG"]/text()').get()  # Название категории
        photo_links = response.xpath('.//a[@class="zNNw1"]/@href').getall()
        for link in photo_links:
            yield response.follow(link, self.parse_photo, meta={'category': category})

    def parse_photo(self, response):
        item = ImageItem()
        item['title'] = response.xpath('//p[@class="liDlw"]/text()').get()
        item['category'] = response.meta['category']
        
        # Извлекаем srcset
        srcset = response.xpath('//div[@class="wdUrX"]/img/@srcset').get()
        self.logger.info(f"Srcset: {srcset}")

        if srcset:
            # Разбиваем srcset на ссылки
            srcset_urls = srcset.split(',')

            # Находим ссылку с максимальным значением параметра 'w'
            max_res_url = max(srcset_urls, key=lambda url: int(url.split('w=')[-1].split('&')[0]))

            # Убираем пробелы и сохраняем ссылку
            item['image_urls'] = [max_res_url.strip().split(' ')[0]]
        else:
            # Альтернативный способ извлечь изображение, если srcset не найден
            item['image_urls'] = response.xpath('//div[@class="wdUrX"]/img/@src').get()

        yield item






