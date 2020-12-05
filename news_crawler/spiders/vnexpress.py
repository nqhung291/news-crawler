#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import os
from codecs import open
import re
import csv

URL = 'https://vnexpress.net/'

# Hash table chưa tên chủ đề, để tạo thư mục
CATEGORIES = {
    'thoi-su': 'Thời sự',
    'the-gioi': 'Thế giới',
    'kinh-doanh': 'Kinh doanh',
    'giai-tri': 'Giải trí',
    'the-thao': 'Thể thao',
    'phap-luat': 'Pháp luật',
    'giao-duc': 'Giáo dục',
    'suc-khoe': 'Sức khoẻ',
    'doi-song': 'Đời sống',
    'khoa-hoc': 'Khoa học',
    'so-hoa': ' Công nghệ',
    'du-lich': 'Du lịch',
}

CATEGORIES_COUNTER = {
    'giao-duc': [0, 0],
    'suc-khoe': [0, 0],
    'khoa-hoc': [0, 0],
    'so-hoa': [0, 0],
    'giai-tri': [0, 0],
    'the-thao': [0, 0],
    'doi-song': [0, 0],
    'du-lich': [0, 0]
}


class VnExpress(scrapy.Spider):
    '''Crawl tin tức từ https://vnexpress.net website
    ### Các tham số:
        category: Chủ đề để crawl, có thể bỏ trống. Các chủ đề
                 * giao-duc
                 * suc-khoe
                 * khoa-hoc
                 * so-hoa
                 * giai-tri
                 * the-thao
                 * doi-song
                 * du-lich
        limit: Giới hạn số trang để crawl, có thể bỏ trống.
    '''
    name = "vnexpress"
    folder_path = "data"
    page_limit = None
    start_urls = []
    crawled_data = []
    filename = 'vnexpress.csv'

    def __init__(self, category=None, limit=None, *args, **kwargs):
        super(VnExpress, self).__init__(*args, **kwargs)
        if limit is not None:
            self.page_limit = int(limit)
        # Tạo thư mục
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

        if category in CATEGORIES:
            self.start_urls = [URL + category]
        else:
            for CATEGORY in CATEGORIES:
                self.start_urls.append(URL + CATEGORY)

    def start_requests(self):
        for url in self.start_urls:
            if self.page_limit:
                for p in range(self.page_limit):
                    if url in ['the-thao', 'doi-song', 'du-lich', 'so-hoa']:
                        page_url = url + '/p' + str(p + 1)
                    else:
                        page_url = url + '-p' + str(p + 1)
                    yield scrapy.Request(url=page_url, callback=self.parse_list_news)

    def parse_list_news(self, response):
        category = self.get_category_from_url(response.url)
        list_articles = response.css('.list-news-subfolder .item-news.item-news-common')
        for article in list_articles:
            title = article.css('.title-news a::text').get()
            content = article.css('.description a::text').get()
            url = article.css('.title-news a::attr(href)').extract_first()
            if title is not None and content is not None:
                fields = [CATEGORIES[category], title.strip(), content.strip(), url]
                with open(self.folder_path + "/" + self.filename, 'a', encoding='utf-8') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(fields)

    def get_category_from_url(self, url):
        items = url.split('/')
        category = None
        if len(items) >= 4:
            category = re.sub(r'-p[0-9]+', '', items[3])
        return category
