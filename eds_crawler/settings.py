# -*- coding: utf-8 -*-

# Scrapy settings for eds_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'eds_crawler'

SPIDER_MODULES = ['eds_crawler.spiders']
NEWSPIDER_MODULE = 'eds_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/64.0'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/64.0',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'eds_crawler.middlewares.EdsCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'eds_crawler.middlewares.EdsCrawlerDownloaderMiddleware': 543,
# }
DOWNLOADER_MIDDLEWARES = {
    'eds_crawler.middlewares.WeiboMiddleware': 543,
}

# # 禁止重定向
# REDIRECT_ENABLED = False

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'eds_crawler.pipelines.AsynchronousMysqlPipeline': 300,
    'eds_crawler.pipelines.MysqlPipeline': 300,
}

# 配置mysql连接信息
MYSQL_HOST = '10.10.192.61'
MYSQL_PORT = 3306
MYSQL_DB = 'ai'
MYSQL_USER = 'ai'
MYSQL_PASSWORD = 'ai_123'
MYSQL_CHARSET = 'utf8'

# 配置redis连接信息
REDIS_HOST = '10.10.32.220'
REDIS_PORT = 6379
REDIS_PASSWORD = 'open'
REDIS_ENCODING = 'utf-8'
REDIS_DECODE_RESPONSES = True


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# 突发事件类型
EDS_TYPE = 5
# 日志路径与日志级别
LOG_FILE = '/data0/search/eds_crawler/logs/weibo_spider_%s.main.log' % EDS_TYPE
LOG_LEVEL = 'INFO'
# LOG_LEVEL = 'DEBUG'

# 设置一个微博爬虫任务的超时时间：5分钟以内
CLOSESPIDER_TIMEOUT = 290

# 爬取最大页数(最大深度)
MAX_PAGE = 12

# 微博登录页
LOGIN_URL = 'https://weibo.cn/pub/'

# PhantomJS路径
PHANTOMJS_PATH = '/application/search/phantomjs/bin/phantomjs'
