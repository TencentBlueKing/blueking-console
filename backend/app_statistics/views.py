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
from builtins import str

from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from analysis.models import AppLiveness, AppOnlineTimeRecord, AppUseRecord
from app.constants import AppStateEnum
from app.models import App
from app.utils import get_users
from app_statistics.utils import (
    get_all_developer,
    get_chart_height,
    get_data_by_time,
    get_format_date,
    get_sorted_category_data,
    get_str_range_time,
    handle_user_select,
    transform_sec_to_hour,
)


def app_statistics_page(request, template_name):
    """
    统计分析首页
    """
    template_path = "app_statistics/%s.html" % template_name
    return render(request, template_path, {})


def get_all_user(request):
    """
    前端用户下拉框所需数据
    """
    all_user = get_users(request)
    return JsonResponse({"result": True, "data": handle_user_select(all_user)})


def get_all_app_developer(request):
    """
    获取所有开发者
    """
    all_app_developer = get_all_developer()
    return JsonResponse({"result": True, "data": handle_user_select(all_app_developer)})


def get_all_app(request):
    """
    前端应用下拉框所需数据
    """
    # 获取所有曾经上过线的应用
    all_app = App.objects.exclude(first_online_time__isnull=True).values("code", "name")
    app_list = [{"id": i["code"], "text": i["name"]} for i in all_app]
    app_list.insert(0, {"id": "", "text": _(u"全部")})
    result = {"result": True, "data": app_list}
    return JsonResponse(result)


def online_time_by_time(request):
    """
    在线时长（按照时间）
    """
    # 获取请求参数
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用
    user_name = request.GET.get("user_name", "")  # 用户
    show_way = int(request.GET.get("show_way", 0))  # 展示方式

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 获取数据
    all_online_time, total_online_time = AppOnlineTimeRecord.objects.get_onlinetime(stime, etime, app_code, user_name)

    # 统计方法定义
    def _computer_data(queryset, st, et):
        secords_sum = queryset.filter(add_date__gte=st, add_date__lt=et).aggregate(sum=Sum("online_time"))["sum"] or 0
        return transform_sec_to_hour(secords_sum)

    category, data = get_data_by_time(_computer_data, all_online_time, show_way, stime, etime)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"在线时长分时间统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total)s 小时）")
        % {"range_time": get_str_range_time(stime, etime), "total": transform_sec_to_hour(total_online_time)},
        "series_name": _(u"在线时长"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def online_time_by_user(request):
    """
    在线时长（按照用户）
    """
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用
    user_name = request.GET.get("user_name", "")  # 用户

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 获取数据
    all_online_time, total_online_time = AppOnlineTimeRecord.objects.get_onlinetime(stime, etime, app_code, user_name)

    # 计算
    user_online_time = all_online_time.values("user__username").annotate(sum=Sum("online_time"))
    category_data = [(i["user__username"], transform_sec_to_hour(i["sum"])) for i in user_online_time]
    # 排序后数据
    category, data = get_sorted_category_data(category_data)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"在线时长分用户统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total_hour)s 小时，用户总数：%(total_user)s）")
        % {
            "range_time": get_str_range_time(stime, etime),
            "total_hour": transform_sec_to_hour(total_online_time),
            "total_user": len(data),
        },
        "series_name": _(u"在线时长"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def online_time_by_app(request):
    """
    在线时长（按照应用）
    """
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用
    user_name = request.GET.get("user_name", "")  # 用户

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 获取数据
    all_online_time, total_online_time = AppOnlineTimeRecord.objects.get_onlinetime(stime, etime, app_code, user_name)

    # 计算
    app_online_time = all_online_time.values("app_code").annotate(sum=Sum("online_time"))

    category_data = [(i["app_code"], transform_sec_to_hour(i["sum"])) for i in app_online_time]
    # 排序后数据
    category, data = get_sorted_category_data(category_data)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"在线时长分应用统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total_hour)s 小时，应用总数：%(total_app)s）")
        % {
            "range_time": get_str_range_time(stime, etime),
            "total_hour": transform_sec_to_hour(total_online_time),
            "total_app": len(data),
        },
        "series_name": _(u"在线时长"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def visit_by_time(request):
    """
    访问量（按照时间）
    """
    # 获取请求参数
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用
    show_way = int(request.GET.get("show_way", 0))  # 展示方式

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)

    # 获取数据
    all_visit, total_visit = AppUseRecord.objects.get_appuserecord(stime, etime, app_code)

    # 统计方法定义
    def _computer_data(queryset, st, et):
        return queryset.filter(use_time__gte=st, use_time__lt=et).count()

    category, data = get_data_by_time(_computer_data, all_visit, show_way, stime, etime)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"访问量分时间统计"),
        "subtitle": _(u"%(range_time)s（总量：%(total)s 次）")
        % {"range_time": get_str_range_time(stime, etime), "total": total_visit},
        "series_name": _(u"访问量"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def visit_by_app(request):
    """
    在线时长（按照应用）
    """
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)

    # 获取数据
    all_visit, total_visit = AppUseRecord.objects.get_appuserecord(stime, etime, app_code)

    # 计算
    app_vist = all_visit.values("app__name").annotate(count=Count("app__name"))
    category_data = [(i["app__name"], i["count"]) for i in app_vist]
    # 排序后数据
    category, data = get_sorted_category_data(category_data)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"访问量分应用统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total_visit)s 次，应用总数：%(total_app)s）")
        % {"range_time": get_str_range_time(stime, etime), "total_visit": total_visit, "total_app": len(data)},
        "series_name": _(u"访问量"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def liveness_by_time(request):
    """
    活跃度（按照时间）
    """
    category = []
    data = []

    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用
    show_way = int(request.GET.get("show_way", 0))  # 展示方式

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 获取数据
    all_liveness, total_liveness = AppLiveness.objects.get_appliveness(stime, etime, app_code)

    # 统计方法定义
    def _computer_data(queryset, st, et):
        return queryset.filter(add_date__gte=st, add_date__lt=et).aggregate(sum=Sum("hits"))["sum"] or 0

    category, data = get_data_by_time(_computer_data, all_liveness, show_way, stime, etime)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"活跃度分时间统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total)s 次）")
        % {"range_time": get_str_range_time(stime, etime), "total": total_liveness},
        "series_name": _(u"活跃度"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def liveness_by_app(request):
    """
    在线时长（按照应用）
    """
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_code = request.GET.get("app_code", "")  # 应用

    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 获取数据
    all_liveness, total_liveness = AppLiveness.objects.get_appliveness(stime, etime, app_code)

    # 计算
    app_liveness = all_liveness.values("app__name").annotate(sum=Sum("hits"))
    category_data = [(i["app__name"], i["sum"]) for i in app_liveness]
    # 排序后数据
    category, data = get_sorted_category_data(category_data)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"活跃度分应用统计"),
        "subtitle": _(u"%(range_time)s （总量：%(total_liveness)s 次，应用总数：%(total_app)s）")
        % {"range_time": get_str_range_time(stime, etime), "total_liveness": total_liveness, "total_app": len(data)},
        "series_name": _(u"活跃度"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def developer_by_developer(request):
    """
    应用负责人（按照开发者）
    """
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    app_developer = request.GET.get("app_developer", "")  # 应用开发者
    app_state = request.GET.get("app_state", "")  # 应用状态

    oneday = datetime.timedelta(days=1)
    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)

    # 查询所有开发者
    all_developer = get_all_developer()
    all_developer = [i["username"] for i in all_developer]

    # 所有应用
    all_app = App.objects.filter(
        created_date__gte=stime, created_date__lt=etime + oneday, is_lapp=False, is_sysapp=False
    )
    # 应用状态筛选
    app_state_list = [
        str(i) for i in [AppStateEnum.OUTLINE, AppStateEnum.DEVELOPMENT, AppStateEnum.TEST, AppStateEnum.ONLINE]
    ]
    if app_state in app_state_list:
        all_app = all_app.filter(state=int(app_state))
    # 应用开发者筛选
    if app_developer:
        all_developer = [app_developer]

    # 统计
    data_list = []
    for i in all_developer:
        num = all_app.filter(Q(developer__username=i), Q(creater=i)).count()
        if num:
            data_list.append((i, num))
    # 排序后数据
    category, data = get_sorted_category_data(data_list)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"开发者开发应用个数统计"),
        "subtitle": _(u"%(range_time)s （开发者总数：%(total_developer)s）")
        % {"range_time": get_str_range_time(stime, etime), "total_developer": len(data)},
        "series_name": _(u"应用个数"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)


def app_update_by_new_online(request):
    """
    应用更新情况（新上线）
    """
    # 获取请求参数
    s_time = request.GET.get("stime")  # 开始时间
    e_time = request.GET.get("etime")  # 截止时间
    show_way = int(request.GET.get("show_way", 0))  # 展示方式

    oneday = datetime.timedelta(days=1)
    # 格式化时间
    stime, etime = get_format_date(s_time, e_time)
    # 所有应用
    all_app = App.objects.filter(
        first_online_time__gte=stime, first_online_time__lt=etime + oneday, is_lapp=False, is_sysapp=False
    )

    # 总时长
    total_app = all_app.count()

    # 统计方法定义
    def _computer_data(queryset, st, et):
        return queryset.filter(first_online_time__gte=st, first_online_time__lt=et).count()

    category, data = get_data_by_time(_computer_data, all_app, show_way, stime, etime)

    ctx = {
        "chart_height": get_chart_height(len(category)),
        "title": _(u"新上线应用数量统计"),
        "subtitle": _(u"%(range_time)s （应用个数：%(total)s 个）")
        % {"range_time": get_str_range_time(stime, etime), "total": total_app},
        "series_name": _(u"新上线应用个数"),
        "category": category,
        "data": data,
    }
    return render(request, "app_statistics/bar_chart.part", ctx)
