# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - 蓝鲸桌面 (BlueKing - bkconsole) available.
Copyright (C) 2022 THL A29 Limited,
a Tencent company. All rights reserved.
Licensed under the MIT License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the
specific language governing permissions and limitations under the License.

We undertake not to change the open source license (MIT license) applicable

to the current version of the project delivered to anyone in the future.
"""
import datetime
from builtins import range, zip

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext as _

from common.log import logger
from common.utils.time import parse_local_datetime


def get_all_developer():
    """
    获取所有开发者中心用户
    """
    # 获取所有的用户信息
    user_model = get_user_model()
    users = user_model.objects.all().values("username", "chname")
    return users


def get_chart_height(data_length):
    """
    计算页面上图表高度
    """
    chart_min_height = 400  # 页面上图表的最小高度
    pre_bar_height = 35  # 横向柱状图表每条柱状的高度
    current_height = data_length * pre_bar_height
    return max(current_height, chart_min_height)


def get_format_date(s_time, e_time):
    """
    获取格式化后的本地时间的日期
    """
    today = timezone.localtime(timezone.now())
    try:
        if e_time:
            etime = parse_local_datetime(e_time.strip() + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        else:
            etime = today

        if s_time:
            stime = parse_local_datetime(s_time.strip(), "%Y-%m-%d")
        else:
            stime = parse_local_datetime("%s-01-01" % today.year, "%Y-%m-%d")
    except Exception as e:
        logger.error("An error occurred in statistical analysis of the time format conversion: %s" % e)
        stime = parse_local_datetime("%s-01-01" % today.year, "%Y-%m-%d")
        etime = today
    return (stime, etime)


def get_first_day_of_next_month(c_time):
    """
    获取下个月第一天
    """
    year = c_time.year if c_time.month < 12 else c_time.year + 1
    month = c_time.month + 1 if c_time.month < 12 else 1
    return parse_local_datetime("%s-%s-01" % (year, month), "%Y-%m-%d")


def get_month_list(s_time, e_time):
    """
    获取s_time - e_time 时间内的月数
    """
    time_list = [s_time]
    n_time = get_first_day_of_next_month(s_time)
    while n_time <= e_time:
        time_list.append(n_time)
        n_time = get_first_day_of_next_month(n_time)
    time_list.append(e_time + datetime.timedelta(days=1))

    return time_list


def get_week_list(s_time, e_time):
    """
    获取s_time - e_time 时间内的周数
    """
    time_list = [s_time]
    n_time = s_time + datetime.timedelta(days=7 - s_time.isocalendar()[2] + 1)
    oneweek = datetime.timedelta(weeks=1)
    while n_time <= e_time:
        time_list.append(n_time)
        n_time += oneweek
    time_list.append(e_time + datetime.timedelta(days=1))

    return time_list


def get_day_list(s_time, e_time):
    """
    获取s_time - e_time 时间内的所有日期
    """
    time_list = []
    oneday = datetime.timedelta(days=1)
    n_time = s_time
    while n_time <= e_time:
        time_list.append(n_time)
        n_time += oneday
    time_list.append(e_time + datetime.timedelta(days=1))

    return time_list


def get_time_list(s_time, e_time, way):
    """
    获取s_time - e_time 时间内的时间
    """
    time_list = []
    if way == 0:
        time_list = get_month_list(s_time, e_time)
    elif way == 1:
        time_list = get_week_list(s_time, e_time)
    elif way == 2:
        time_list = get_day_list(s_time, e_time)

    return time_list


def get_str_range_time(stime, etime):
    """
    获取需要展示的时间字符串
    """
    return u"%s ~ %s" % (stime.strftime("%Y-%m-%d"), etime.strftime("%Y-%m-%d"))


def transform_sec_to_hour(secords):
    """
    秒转小时
    """
    return round(secords / 3600.0, 2)


def get_categories_str(dtime, way):
    """
    获取时间轴字符串格式
    """
    categories_str = ""
    if way == 0:
        categories_str = _(u"%(year)s年%(month)s月") % {"year": dtime.year, "month": dtime.month}
    elif way == 1:
        week = dtime.isocalendar()
        categories_str = _(u"%(year)s年%(week)s周") % {"year": week[0], "week": week[1]}
    elif way == 2:
        categories_str = _(u"%(year)s年%(month)s月%(day)s日") % {
            "year": dtime.year,
            "month": dtime.month,
            "day": dtime.day,
        }
    return categories_str


def get_data_by_time(func, queryset, show_way, stime, etime):
    """
    通用时间统计，主要是根据不同时间展示方式计算数据
    """
    category = []
    data = []
    # 获取时间范围内所有时间
    time_list = get_time_list(stime, etime, show_way)
    time_len = len(time_list) - 1
    for i in range(time_len):
        # 获取时间展示字符串
        categories_str = get_categories_str(time_list[i], show_way)
        # 动态计算数据
        cnt = func(queryset, time_list[i], time_list[i + 1])
        category.append(categories_str)
        data.append(cnt)
    return category, data


def handle_user_select(all_person):
    """
    处理名字下拉框所需数据
    """
    user_list = [{"id": i["username"], "text": i["username"]} for i in all_person]
    user_list.insert(0, {"id": "", "text": _(u"全部")})
    return user_list


def get_sorted_category_data(category_data, reverse=False):
    """
    获取按照data排序的category_data
    """
    # 排序
    category_data.sort(key=lambda x: x[1], reverse=reverse)
    category, data = list(zip(*category_data)) if category_data else ([], [])
    return category, data
