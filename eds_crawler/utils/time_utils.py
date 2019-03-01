#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : pureoym
# @Contact : pureoym@163.com
# @TIME    : 2019/2/18 18:08
# @File    : time_util.py
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
import datetime
import re


def get_current_datetime():
    """
    获取当前时间
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_pubtime(time_string):
    """
    根据输入的时间字符串获取发布时间
    :param time_string:
    :return:
    """
    now_time = datetime.datetime.now()
    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        publish_time = now_time - datetime.timedelta(minutes=int(minutes))
        return publish_time.strftime('%Y-%m-%d %H:%M:%S')

    if '小时前' in time_string:
        hours = re.search(r'^(\d+)小时', time_string).group(1)
        publish_time = now_time - datetime.timedelta(hours=int(hours))
        return publish_time.strftime('%Y-%m-%d %H:%M:%S')

    if '今天' in time_string:
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    return time_string


def is_expired(update_time, expire_day):
    """
    判断cookie是否过期，如果过期则更新cookie
    判断逻辑：
    如果没有更新时间，则判断为过期；
    如果有更新时间，其当前时间大于截止时间，则判断为过期；
    否则为不过期。
    （截止时间 = 更新时间 + 过期日数）
    :param update_time:
    :param expire_day:
    :return:
    """
    if update_time is None:
        return True
    if update_time == '0000-00-00 00:00:00':
        return True
    if update_time is not None:
        current_time = datetime.datetime.now()
        deadline = update_time + datetime.timedelta(days=int(expire_day))
        if current_time > deadline:
            return True
    return False
