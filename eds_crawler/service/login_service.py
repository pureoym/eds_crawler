#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : pureoym
# @Contact : pureoym@163.com
# @TIME    : 2019/2/25 8:45
# @File    : login_service.py
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

import sys

sys.path.append('/application/search/eds_crawler')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from eds_crawler.utils import mysql_utils, time_utils
from scrapy.utils.project import get_project_settings
import time

settings = get_project_settings()
# PHANTOMJS_PATH = settings['PHANTOMJS_PATH']
# LOGIN_URL = settings['LOGIN_URL']
LOGIN_URL = 'https://weibo.cn/pub/'
PHANTOMJS_PATH = '/application/search/phantomjs/bin/phantomjs'
TABLE_NAME = 'eds_weibo_login'


def get_one_cookie(eds_type):
    """
    从mysql库中获取一个可用的cookie
    :return:
    """
    sql = "SELECT `cookie` FROM %s WHERE `eds_type` = %s" \
          % (TABLE_NAME, eds_type)
    cookie_str = mysql_utils.read(sql)[0][0]  # 还未增加随机逻辑
    cookies = cookie_str_to_dict(cookie_str)
    return cookies


def cookie_str_to_dict(cookie_str):
    """
    cookie从字符串转换成字典
    :param cookie_str:
    :return:
    """
    cookies = {}
    if cookie_str is not None and len(cookie_str) > 0:
        cookie_list = cookie_str.split(';')
        if cookie_list is not None and len(cookie_str) > 0:
            for one in cookie_list:
                key = one.strip().split('=')[0]
                value = one.strip().split('=')[1]
                cookies[key] = value
    return cookies


def cookie_list_to_str(cookie_list):
    """
    浏览器获取的cookie转换成库中的格式
    :param cookie_list:
    :return:
    """
    l2 = list(map(lambda x: x['name'] + '=' + x['value'], cookie_list))
    cookie_str = ';'.join(l2)
    return cookie_str


def process():
    """
    微博账号登录信息更新处理。
    处理逻辑：
    1 获取所有微博登录信息(uid,username,password,update_time,expire_time)
    2 根据更新逻辑获取需要更新的更新列表
    3 爬取新的登录信息（cookie）
    4 更新登录信息
    :return:
    """
    # 获取所有微博登录信息(uid,username,password,update_time,expire_time)
    items = get_login_items()

    # 根据更新逻辑获取需要更新的更新列表
    items_with_cookies = check_update(items)

    # 更新登录信息
    update_login_items(items_with_cookies)


def get_login_items():
    """
    获取所有微博登录信息(uid,username,password,update_time,expire_time)
    :return:
    """

    sql = 'SELECT `uid`,`username`,`password`,`update_time`,`expire_day` FROM %s ' \
          % TABLE_NAME
    items = mysql_utils.read(sql)
    return items


def check_update(items):
    """
    获取需要更新cookie的登录信息
    :param items:
    :return:
    """
    output_items = []
    for item in items:
        uid = item[0]
        username = item[1]
        password = item[2]
        update_time = item[3]
        expire_day = item[4]
        expired = time_utils.is_expired(update_time, expire_day)
        if expired:
            cookies = crawl_cookie(username, password)
            current_time = time_utils.get_current_datetime()
            output_items.append((uid, cookies, current_time))
    return output_items


def crawl_cookie(username, password):
    """
    根据用户名和密码获取cookie
    :param uid:
    :param password:
    :return:
    """
    # 打开浏览器
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS(PHANTOMJS_PATH)

    # 进入未登录状态的微博列表页
    driver.get(LOGIN_URL)
    # 点击登录按钮
    driver.find_element_by_xpath('//a[text()="登录"]').click()
    time.sleep(1)

    # 进入登录页
    WebDriverWait(driver, 30).until(
        EC.title_is('登录 - 新浪微博')
    )
    print('进入登录页')
    time.sleep(1)

    # 进入登录页后，输入用户名密码并点击登录
    driver.find_element_by_id("loginName").clear()
    driver.find_element_by_id("loginName").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("loginPassword").clear()
    driver.find_element_by_id("loginPassword").send_keys(password)
    time.sleep(2)
    driver.find_element_by_id("loginAction").click()

    # 进入列表页
    WebDriverWait(driver, 30).until(
        EC.title_is('我的首页')
    )
    print('进入我的首页')
    time.sleep(5)

    # 获取cookie
    cookies = driver.get_cookies()
    cookies_str = cookie_list_to_str(cookies)
    time.sleep(5)

    # 关闭浏览器
    driver.quit()

    return cookies_str


def update_login_items(items):
    """
    更新微博登录信息（cookie，update_time）
    :param items:
    :return:
    """
    for item in items:
        uid = item[0]
        cookie = item[1]
        update_time = item[2]
        sql = "UPDATE %s SET cookie='%s',update_time='%s' WHERE uid='%s'" \
              % (TABLE_NAME, cookie, update_time, uid)
        mysql_utils.write(sql)
        print('update weibo login items, uid=%s' % uid)


# class WeiboLogin():
#     def __init__(self, username, password):
#         os.system('pkill -f phantom')
#         self.url = LOGIN_URL
#         self.browser = webdriver.PhantomJS(PHANTOMJS_PATH)
#         self.browser.set_window_size(1050, 840)
#         self.wait = WebDriverWait(self.browser, 20)
#         self.username = username
#         self.password = password
#
#     def open(self):
#         """
#         打开网页输入用户名密码并点击
#         :return: None
#         """
#         self.browser.get(self.url)
#         username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
#         password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
#         submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
#         username.send_keys(self.username)
#         password.send_keys(self.password)
#         submit.click()
#
#     def run(self):
#         """
#         破解入口
#         :return:
#         """
#         self.open()
#         WebDriverWait(self.browser, 30).until(
#             EC.title_is('我的首页')
#         )
#         cookies = self.browser.get_cookies()
#         cookie = [item["name"] + "=" + item["value"] for item in cookies]
#         cookie_str = '; '.join(item for item in cookie)
#         self.browser.quit()
#         return cookie_str


def test():
    from selenium import webdriver
    d = webdriver.Chrome()
    d.get('https://www.baidu.com')
    d.find_element_by_id('kw').send_keys('fm.887')
    d.find_element_by_id('su').click()


if __name__ == '__main__':
    process()
    # result = str(mysql_utils.read('select * from eds_weibo_login'))
    # print(result)
    # username = '123'
    # password = '123'
    # crawl_cookie(username, password)
