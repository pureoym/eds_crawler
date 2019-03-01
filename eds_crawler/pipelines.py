# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings
from twisted.enterprise import adbapi


class EdsCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


# import pymongo
#
# class MongoPipeline(object):
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         collection_name = item.__class__.__name__
#         self.db[collection_name].insert(dict(item))
#         return item


class MysqlPipeline(object):
    """
    同步MYSQL连接管道
    """

    def __init__(self):
        settings = get_project_settings()
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        sql = """
        INSERT INTO eds_raw_weibo_data(`wid`,`weibo_url`,`content`,`pic`,`uid`,
        `from_uid`,`from_wid`,`publish_time`,`crawl_time`,`zan`,`transfer`,`comment`)
         VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(
            sql,
            (item['wid'], item['weibo_url'], item['content'], item['pic'],
             item['uid'], item['from_uid'], item['from_wid'], item['publish_time'],
             item['crawl_time'], item['zan'], item['transfer'], item['comment'])
        )
        self.connect.commit()
        return item


class AsynchronousMysqlPipeline(object):
    """
    异步MYSQL连接管道
    """

    def __init__(self, pool):
        self.dbpool = pool

    @classmethod
    def from_settings(cls, settings):
        """
        当爬虫启动时，scrapy调用该函数加载配置
        :param settings:
        :return:
        """
        params = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['MYSQL_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )

        # 创建一个数据库连接池对象，这个连接池中可以包含多个connect连接对象。
        # 参数1：操作数据库的包名
        # 参数2：数据库的连接参数
        db_connect_pool = adbapi.ConnectionPool('pymysql', **params)

        # 初始化这个类的对象
        obj = cls(db_connect_pool)
        return obj

    def process_item(self, item, spider):
        """
        使用twisted异步执行数据库操作。
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addCallback(self.handle_error)

    def do_insert(self, cursor, item):
        """
        数据库插入操作
        :param cursor:
        :param item:
        :return:
        """
        # 对数据库进行插入操作，不需要commit，twisted会自动commit
        sql = """
        INSERT INTO eds_raw_weibo_data(`wid`,`weibo_url`,`content`,`pic`,`uid`,
        `from_uid`,`from_wid`,`publish_time`,`crawl_time`,`zan`,`transfer`,`comment`)
         VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(
            sql,
            (item['wid'], item['weibo_url'], item['content'], item['pic'],
             item['uid'], item['from_uid'], item['from_wid'], item['publish_time'],
             item['crawl_time'], item['zan'], item['transfer'], item['comment'])
        )

    def handle_error(self, failure):
        if failure:
            print(failure)
