#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : pureoym
# @Contact : pureoym@163.com
# @TIME    : 2019/2/22 10:48
# @File    : mysql_utils.py
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
import pymysql
from DBUtils.PooledDB import PooledDB
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
# pool = PooledDB(creator=pymysql,
#                 maxconnections=10,
#                 host=settings['MYSQL_HOST'],
#                 port=settings['MYSQL_PORT'],
#                 database=settings['MYSQL_DB'],
#                 user=settings['MYSQL_USER'],
#                 password=settings['MYSQL_PASSWORD'],
#                 charset=settings['MYSQL_CHARSET'], )
pool = PooledDB(creator=pymysql,
                maxconnections=10,
                host='10.10.192.61',
                port=3306,
                database='ai',
                user='ai',
                password='ai_123',
                charset='utf8', )


def read(sql):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    finally:
        conn.close()
    return result


def write(sql):
    try:
        conn = pool.connection()
        cursor = conn.cursor()
        count = cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()
    return count
