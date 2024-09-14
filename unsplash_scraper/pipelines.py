# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from itemadapter import ItemAdapter


# class UnsplashScraperPipeline:
#     def process_item(self, item, spider):
#         return item

# import csv

# class ImageCSVWriterPipeline:
#     def open_spider(self, spider):
#         # Открываем файл с кодировкой utf-8
#         self.file = open('images.csv', 'w', newline='', encoding='utf-8')
#         self.writer = csv.DictWriter(self.file, fieldnames=['image_url', 'image_path', 'title', 'category'])
#         self.writer.writeheader()

#     def close_spider(self, spider):
#         self.file.close()
#         spider.logger.info("CSV file closed")
        
#     def process_item(self, item, spider):
#         # Проверяем, что изображение успешно скачано
#         if 'images' in item and item['images']:
#             image_path = item['images'][0]['path']
#             full_image_path = f"{spider.settings.get('IMAGES_STORE', '')}/{image_path}"
#             self.writer.writerow({
#                 'image_url': item['image_urls'][0],
#                 'image_path': full_image_path,
#                 'title': item['title'],
#                 'category': item.get('category', 'N/A')
#             })
#             spider.logger.info(f"Item written to CSV: {item}")
#         else:
#             spider.logger.warning(f"Item does not have images: {item}")
#         return item

import csv
from scrapy.pipelines.images import ImagesPipeline  # Импортируем ImagesPipeline
from scrapy import Request

class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        # Возвращаем локальный путь для сохранения изображения
        return f"{item['category']}/{item['title']}.jpg"

    def get_media_requests(self, item, info):
        # Этот метод делает запрос на скачивание изображения
        for image_url in item.get('image_urls', []):
            yield Request(image_url)

    def item_completed(self, results, item, info):
        # Сохраняем дополнительные данные в CSV после загрузки изображения
        image_path = [x['path'] for ok, x in results if ok]
        if image_path:
            item['image_path'] = image_path[0]

            # Записываем данные в CSV
            with open('images_data.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([item['image_urls'][0], item['image_path'], item['title'], item['category']])

        return item





