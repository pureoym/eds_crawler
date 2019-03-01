#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : pureoym
# @Contact : pureoym@163.com
# @TIME    : 2019/2/19 17:11
# @File    : redis_utils.py
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
import redis
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
pool = redis.ConnectionPool(host=settings['REDIS_HOST'],
                            port=settings['REDIS_PORT'],
                            password=settings['REDIS_PASSWORD'],
                            encoding=settings['REDIS_ENCODING'],
                            decode_responses=settings['REDIS_DECODE_RESPONSES'])


def get(key):
    rdc = redis.StrictRedis(connection_pool=pool)
    return rdc.get(key)


def set(key, value):
    rdc = redis.StrictRedis(connection_pool=pool)
    return rdc.set(key, value)
