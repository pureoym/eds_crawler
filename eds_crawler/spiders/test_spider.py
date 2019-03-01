#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : pureoym
# @Contact : pureoym@163.com
# @TIME    : 2019/1/16 15:21
# @File    : quotes_spider.py
# Copyright 2017 pureoym. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import scrapy
from eds_crawler.utils import redis_utils


class TestSpider(scrapy.Spider):
    """
    TestSpider
    """
    # 爬虫唯一标识：微博爬虫
    name = "test"
    allowed_domains = ['163.com', 'sports.163.com']

    start_urls = ['http://sports.163.com/yc/']

    def parse(self, response):
        self.logger.info('this is item page! %s' % response.url)

        # news_list = response.css(
        #     'body > div > div.ne-area > div.area.clearfix > div.middle_part > div.topnews_block > div')

        import time
        for i in range(10):
            t1 = int(round(time.time() * 1000))

            # sql = "SELECT password FROM eds_crawler_login WHERE uid = '6603369153'"
            # r = mysql_utils.execute_sql(sql)

            print(redis_utils.get('eds_crawler_update_flag'))
            t2 = int(round(time.time() * 1000))
            print(t2 - t1)



            # for news in news_list:
            #     item = TestItem()
            #     item['title'] = news.css('h2 > a::text').extract_first()
            #     item['url'] = news.css('h2 > a::attr(href)').extract_first()
            #     # yield item
            #     redis_utils
