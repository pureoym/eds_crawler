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
from eds_crawler.items import WeiboItem
from scrapy.http import Request
from eds_crawler.utils import time_utils, redis_utils
from scrapy.utils.project import get_project_settings

# from scrapy.crawler import CrawlerProcess

settings = get_project_settings()
MAX_PAGE = settings['MAX_PAGE']
EDS_TYPE = settings['EDS_TYPE']


class WeiboSpider(scrapy.Spider):
    """
    微博数据爬虫
    """

    # 爬虫唯一标识：微博爬虫
    name = "weibo_spider_%s" % EDS_TYPE
    allowed_domains = ['weibo.cn', 'passport.weibo.cn']

    # 可以从多个用户的关注列表中获取这些用户的关注对象信息和关注对象的微博信息
    start_urls = ['https://weibo.cn']
    url = 'https://weibo.cn'

    def parse(self, response):
        """
        解析
        :param response:
        :return:
        """
        self.logger.info('weibo_spider parse start, url=[%s]' % response.url)

        # 获取下一页并解析
        # 增量更新逻辑如下：
        # 获取redis中获取更新标志字段update_flag，该字段值为上次更新最新微博ID。
        # 在本次爬虫解析数据中，如果本页页面中不出现该微博ID，则爬取下一页数据；否则，不爬取下一页。
        # 默认本次微博更新将数据更新至最新，用本次微博更新的最新微博ID，更新update_flag值
        next_page = response.xpath('//*[@id="pagelist"]/form/div/a[text()="下页"]/@href').extract_first()
        current_weibo_id_list = response.xpath('//div[starts-with(@id,"M_")]/@id').extract()
        current_weibo_id_list = list(map(lambda x: x.replace('M_', ''), current_weibo_id_list))
        if '?since_id=0&' in next_page:
            current_newest_weibo_id = response.xpath('//div[starts-with(@id,"M_")]/@id').extract_first()
            current_newest_weibo_id = current_newest_weibo_id.replace('M_', '')
        else:
            current_newest_weibo_id = ''
        # print('response.meta before')
        # print(response.meta)
        if current_newest_weibo_id is not None and len(current_newest_weibo_id) > 0:
            response.meta['current_newest_weibo_id'] = current_newest_weibo_id
        # print('response.meta after')
        # print(response.meta)

        # 从redis中读取上次最后更新的数据
        update_flag = redis_utils.get('eds_crawler_update_flag')
        # self.logger.info('redis.eds_crawler_update_flag = %s' % update_flag)
        # self.logger.info('current_weibo_id_list = %s' % current_weibo_id_list)
        if next_page is not None:  # 如果含有下一页
            page_num = int(next_page.split('&page=')[1])
            if page_num <= MAX_PAGE:
                need_parse_next_page = update_flag not in current_weibo_id_list
                # self.logger.info('need_parse_next_page = %s' % need_parse_next_page)
                if need_parse_next_page:  # 如果update_flag不在当前页的微博ID列表中
                    # 进入下一页并解析
                    next_page_url = 'https://weibo.cn/%s' % next_page
                    yield Request(next_page_url, self.parse, dont_filter=False, meta=response.meta)
                else:  # 如果不需要爬取下一页，那么更新标签
                    # 如果微博ID为最新ID，则更新update_flag值
                    current_newest_weibo_id = response.meta['current_newest_weibo_id']
                    result = redis_utils.set('eds_crawler_update_flag', current_newest_weibo_id)  # 保存redis参数
                    self.logger.info('update redis eds_crawler_update_flag = %s, result = %s'
                                     % (current_newest_weibo_id, result))
            else:  # 如果到达最大页数，则更新标签
                current_newest_weibo_id = response.meta['current_newest_weibo_id']
                result = redis_utils.set('eds_crawler_update_flag', current_newest_weibo_id)  # 保存redis参数
                self.logger.info('update redis eds_crawler_update_flag = %s, result = %s'
                                 % (current_newest_weibo_id, result))

        # 解析本页信息
        weibo_list = response.xpath('//div[starts-with(@id,"M_")]')
        for weibo in weibo_list:
            try:
                weibo_item = WeiboItem()
                # 获取微博主键字段wid
                wid = weibo.xpath('.//@id').extract_first().replace('M_', '')

                # 增加中断解析判断逻辑，
                # 如果当前item中的微博ID等于update_flag，则此item与该页面之后的item不继续解析入库
                if wid == update_flag:
                    break

                weibo_item['wid'] = wid
                weibo_item['weibo_url'] = "https://weibo.cn/comment/%s" % wid

                # 获取图片字段
                pic_flag = weibo.xpath('.//a[text()="原图"]')
                if pic_flag:
                    weibo_item['pic'] = weibo.xpath('.//a[text()="原图"]/@href').extract_first().strip()
                else:
                    weibo_item['pic'] = None

                # 获取用户ID字段
                uid_url = weibo.xpath('//div/a[@class="nk"]/@href').extract_first().strip()
                # uid = uid_url.replace('https://weibo.cn/u/', '')
                weibo_item['uid'] = uid_url

                # 获取转发自用户ID字段，转发自微博ID字段
                weibo_item['from_uid'] = None
                weibo_item['from_wid'] = None

                # 获取发布时间字段
                publish_time_str = weibo.xpath('//div/span[@class="ct"]/text()').extract_first().strip()
                if "来自" in publish_time_str:
                    weibo_item['publish_time'] = time_utils.get_pubtime(publish_time_str.split('来自')[0].strip())
                else:
                    weibo_item['publish_time'] = time_utils.get_pubtime(publish_time_str)

                # 设置爬取时间字段
                weibo_item['crawl_time'] = time_utils.get_current_datetime()

                # 其他字段
                weibo_item['zan'] = None
                weibo_item['transfer'] = None
                weibo_item['comment'] = None

                # 获取正文字段content
                # 检验有没有阅读全文。如果有，正文从详情面中获取；否则，直接从当前页面获取正文
                full_text_flag = weibo.xpath('.//a[text()="全文"]')
                if full_text_flag:
                    detail_page_url = "https://weibo.cn/comment/%s" % wid
                    yield Request(detail_page_url, callback=self.parse_detail_page,
                                  meta={'item': weibo_item}, priority=1)
                else:
                    content = weibo.xpath("string(div)").extract_first(default="").strip()
                    weibo_item['content'] = content
                    yield weibo_item

            except Exception as e:
                self.logger.error(e)

    def parse_detail_page(self, response):
        """
        解析详情页的信息
        :param response:
        :return:
        """
        weibo_item = response.meta['item']
        scope = response.xpath('//div[@id="M_"]')
        content = scope.xpath("string(div)").extract_first(default="").strip()
        weibo_item['content'] = content
        yield weibo_item

# if __name__ == '__main__':
#     process = CrawlerProcess(get_project_settings())
#     process.crawl('weibo_spider')
#     process.start()
