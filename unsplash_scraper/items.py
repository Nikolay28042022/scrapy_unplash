# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()  # Ссылка на изображение Это поле будет использоваться ImagesPipeline
    images = scrapy.Field()  # Сохраненные изображения  ImagesPipeline будет сохранять данные о скачанных изображениях
    title = scrapy.Field()  # Название изображения
    category = scrapy.Field()  # Категория изображения
    image_path = scrapy.Field()  # Локальный путь к изображению

