#!/usr/bin/env bash
pid=`ps -ef|grep 'scrapy crawl weibo_spide'|grep -v grep|awk '{print $2}'`
if [[ $pid -le 0 ]];then
    cd /application/search/eds_crawler
    /application/search/anaconda3/bin/scrapy crawl weibo_spider_5
else
    echo "weibo_spider process running..."
fi
