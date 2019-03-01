# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WeiboItem(Item):
    """
    微博数据元数据类
    """
    # 微博参数
    wid = Field()
    weibo_url = Field()
    content = Field()
    pic = Field()
    uid = Field()
    from_uid = Field()
    from_wid = Field()
    publish_time = Field()
    crawl_time = Field()
    zan = Field()
    transfer = Field()
    comment = Field()
    # server = socket.gethostname()
    # time = datetime.datetime.now()

    # 爬虫参数
    crawl_ip = Field()


class WeiboAccountItem(Item):
    """
    微博账号元数据类
    """
    waid = Field()
    name = Field()
    wa_type = Field()
    location = Field()



class TestItem(Item):
    """
    测试
    """
    title = Field()
    url = Field()
