# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making
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
import operator
from functools import reduce

from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone, translation
from django.utils.translation import ugettext as _

from analysis.models import AppUseRecord
from app.models import App, AppTags
from common.constants import DESKTOP_DEFAULT_APP_HEIGHT, DESKTOP_DEFAULT_APP_WIDTH
from common.exceptions import ConsoleErrorCodes
from common.log import logger
from desktop.constants import BK_CREATOR_TAG_LIST, BK_CREATOR_TAG_STR_LIST, CREATOR_TAG_DICT, AppCreatorTagEnum
from desktop.market_utils import get_market_nav_and_tag_list
from desktop.models import UserApp, UserSettings
from desktop.utils import get_app_logo_url, get_visiable_labels
from release.models import Record as App_release_record
from release.models import Version as App_version


def market(request):
    """
    应用市场
    """
    # 如果有参数id，则表示进入market中某个APP的详细信息
    app_id = int(request.GET.get("id", 0))  # realappid
    # 带搜索参数
    searchkey = request.GET.get("searchkey")
    # 根据用户配置，获取用户应用市场左侧导航配置和分类列表
    market_nav, tag_list = get_market_nav_and_tag_list(request.user.username)
    return render(
        request,
        "desktop/market.html",
        {"app_id": app_id, "searchkey": searchkey, "tag_list": tag_list, "market_nav": market_nav},
    )


def set_market_nav(request):
    """
    设置应用市场左侧导航
    """
    market_nav = int(request.POST.get("market_nav", 1))
    result = UserSettings.objects.update_user_market_nav(request.user, market_nav)
    return JsonResponse({"result": result})


def _get_user_apps(user):
    # 查询所有用户添加的用户
    _all_user_app = UserApp.objects.filter(
        app__state__gt=1, app__is_already_online=True, user=user, desk_app_type=0
    ).values("app__code", "id")
    all_user_app = {i["app__code"]: i["id"] for i in _all_user_app}
    return all_user_app


def _get_hot_apps():
    # 获取应用访问量
    # 查询当前月份 应用访问
    date_time_now = timezone.localtime(timezone.now())
    date_time_one = timezone.make_aware(datetime.datetime(date_time_now.year, date_time_now.month, 1))

    # 查询应用当月访问量
    hot_app = (
        AppUseRecord.objects.filter(use_time__gte=date_time_one, use_time__lte=date_time_now)
        .values("app__code")
        .annotate(num=Count("app__code"))
    )
    hot_app_dict = {i["app__code"]: i["num"] for i in hot_app}
    return hot_app_dict


def _make_query(username, search_tag, search_other):

    # 所有应用（过滤已下架应用（state=0）、开发中应用（state=1））
    all_app = App.objects.filter(state__gt=1, is_already_online=True)

    # 筛选创建者类型
    if search_tag == AppCreatorTagEnum.EEUSER:
        # 筛选企业用户自建的应用
        all_app = all_app.filter(is_saas=False, is_platform=False)
    elif search_tag == AppCreatorTagEnum.OTHER:
        # 筛选其他企业，不在默认蓝鲸服务商和自建中的应用
        all_app = all_app.filter(is_saas=True).exclude(creater__in=BK_CREATOR_TAG_STR_LIST)
    elif search_tag in BK_CREATOR_TAG_LIST:
        # 筛选 蓝鲸或者蓝鲸服务商的应用
        all_app = all_app.filter(creater=CREATOR_TAG_DICT[search_tag])

    # 筛选 应用分类
    app_tag = AppTags.objects.get_tags_by_100id(search_tag)
    if app_tag:
        all_app = all_app.filter(tags=app_tag)

    # NOTE: 2019-08-09 remove 根据开发者搜索 => bk-iam能获取用户的应用列表? 无法模糊匹配
    # 按应用名称, 应用ID, 开发者搜索 -> 按应用名称, 应用ID, 开发负责人搜索

    # 过滤搜索
    if search_other:
        # 组装搜索框中多个搜索条件
        all_app = all_app.filter(
            Q(code__icontains=search_other)
            | Q(name__icontains=search_other)
            | Q(creater__icontains=search_other)
            # Q(developer__username__icontains=search_other) |
            # Q(developer__chname__icontains=search_other) |
        )

    # via username to fetch user_id / [dpid1, dpid2, dpid3]
    visiable_labels = get_visiable_labels(username)
    if not visiable_labels:
        logger.error("get visiable_labels from usermgr fail!")
        # return None
        # NOTE: return no visiable labels apps instead of empty
        all_app = all_app.filter(Q(visiable_labels__isnull=True) | Q(visiable_labels__exact=""))
    else:
        all_app = all_app.filter(
            Q(visiable_labels__isnull=True)
            | Q(visiable_labels__exact="")
            | (reduce(operator.or_, [Q(visiable_labels__icontains=label) for label in visiable_labels]))
        )

    all_app = all_app.distinct()
    return all_app


def market_get_list(request):
    """
    应用市场APP查询（分页查询）
    """
    # 参数处理
    try:
        start_index = int(request.GET.get("from", 0))  # 该页显示数据起始
        end_index = int(request.GET.get("to", 7))  # 该页显示数据结束
        search_tag = int(request.GET.get("sidebar_select", "0"))  # 根据标签查询（'0'： 全部应用，'1': 我的应用， '2': 普通应用, '3': 内置应用）
        search_use = int(request.GET.get("topbar_select", "1"))  # 根据使用指标等查询(1:最新应用，2:最热应用)
        search_other = request.GET.get("keyword", "").strip()  # 搜索框（根据应用name、code等搜索）
    except Exception as error:
        error_message = "%s, App market APP query (paging query) failed, Error message: %s" % (
            ConsoleErrorCodes.E1303101_MARKET_APP_QUERY_FAIL,
            error,
        )
        logger.error(error_message)
        app_info_list = []
        total = 0
        return JsonResponse({"app_info_list": app_info_list, "total": total})

    username = request.user.username
    try:
        all_app = _make_query(username, search_tag, search_other)
        if not all_app:
            app_info_list = []
            total = 0
            return JsonResponse({"app_info_list": app_info_list, "total": total})

        # 应用总数
        total = all_app.count()

        # 过滤指标
        hot_app_dict = _get_hot_apps()
        if search_use == 1 and search_tag != 1:
            # 最新应用（按照首次上线排序）
            all_app = all_app.order_by("-first_online_time")
        elif search_use == 2 and search_tag != 1:
            # 最热门应用（按照每月访问量）
            hot_app_list = [(i, hot_app_dict.get(i.code, 0)) for i in all_app]
            hot_app_list.sort(key=lambda obj: obj[1], reverse=True)
            all_app = [i[0] for i in hot_app_list]

        # 组装数据
        all_user_app = _get_user_apps(request.user)
        all_app_limit = all_app[start_index:end_index]

        app_info_list = []  # 应用信息列表
        is_en = translation.get_language() == "en"
        for app in all_app_limit:
            # 自建应用展示开发者，SaaS应用或者蓝鲸提供应用展示创建者
            developers_value_name = app.creater_display
            # NOTE 2020-04-14 don't query developers from db, while the iam can't get the developers too
            # if not app.is_saas and not app.is_platform:
            #     # TODO: fix here, should get developers from iam or ?
            #     # 获取开发者信息(取前2个)
            #     developers_value_name_list = app.developer.all().values_list('username', flat=True)[0:2]
            #     developers_value_name = ';'.join(developers_value_name_list) if developers_value_name_list else '--'

            app_name = app.name_display
            introduction = app.introduction_display
            if is_en:
                app_name = app.name_en or app.name_display
                introduction = app.introduction_en or app.introduction_display

            app_info = {
                "name": app_name,  # 应用名称
                "code": app.code,  # 应用编码
                "introduction": introduction,  # 应用简介
                "use_count": app.use_count,  # 应用人气数
                "user_app_id": all_user_app.get(app.code, "") if app.code in all_user_app else "",  # 应用对应的user_app id
                "relapp_id": app.id,  # 应用id
                "logo_url": get_app_logo_url(app.code),  # 应用logo
                "developer": developers_value_name if developers_value_name else "--",  # 开发负责人
                "is_saas": app.is_saas,  # 是否SaaS应用
                "is_has": app.code in all_user_app,  # 用户是否添加该应用
                "app_visit_count": hot_app_dict.get(app.code, 0),  # 月访问量
                "islapp": app.is_lapp,  # 是否轻应用
            }
            app_info_list.append(app_info)
    except Exception as error:
        error_message = "%s, App market APP query (paging query) failed, Error message: %s" % (
            ConsoleErrorCodes.E1303101_MARKET_APP_QUERY_FAIL,
            error,
        )
        logger.error(error_message)
        app_info_list = []
        total = 0
    return JsonResponse({"app_info_list": app_info_list, "total": total})


def market_app_detail(request, app_id):
    """
    应用市场APP详细页面
    app_id: app的id
    """
    app_info = {}  # 该应用基本信息
    app_version_list = []  # 应用版本信息
    try:
        app = App.objects.get(id=app_id)
        # 查询本月访问量
        date_time_now = timezone.localtime(timezone.now())
        date_time_one = timezone.make_aware(datetime.datetime(date_time_now.year, date_time_now.month, 1))
        app_visit_count = AppUseRecord.objects.filter(
            app=app, use_time__gte=date_time_one, use_time__lte=date_time_now
        ).count()
        # 开发负责人
        # developers_value_name_list = app.developer.all().values_list('username', flat=True)
        # developers_value_name = ';'.join(developers_value_name_list)

        # get developers from iam
        developers_value_name = ""
        if not (app.is_saas or app.is_platform):
            # app_developers = Permission().app_developers(app.code)
            # developers_value_name = subjects_display(app_developers)
            developers_value_name = ""
        else:
            pass
            # app_developers = []

        try:
            newst_online_time = (
                App_release_record.objects.filter(app_code=app.code, operate_id=1, is_success=True)
                .latest("operate_time")
                .operate_time
            )
        except Exception:
            newst_online_time = "--"

        is_en = translation.get_language() == "en"
        app_name = app.name_display
        introduction = app.introduction_display
        if is_en:
            app_name = app.name_en or app.name_display
            introduction = app.introduction_en or app.introduction_display

        app_info = {
            "app_id": app.id,
            "name": app_name,
            "code": app.code,
            "tag": app.tag_name,
            "use_count": app.use_count,
            "width": "%s px" % (app.width if app.width else DESKTOP_DEFAULT_APP_WIDTH),
            "height": "%s px" % (app.height if app.height else DESKTOP_DEFAULT_APP_HEIGHT),
            "is_max": _(u"是") if app.is_max else _(u"否"),
            "is_saas": app.is_saas,
            "is_third": app.is_third,
            "is_platform": app.is_platform,
            "introduction": introduction,
            "creater": app.creater_display,
            "developer": developers_value_name,
            "display_type": "app",
            "first_test_time": app.first_test_time or "--",
            "first_online_time": app.first_online_time or "--",
            "newst_online_time": newst_online_time,
            "logo_url": get_app_logo_url(app.code),
            "issetbar": _(u"是") if app.is_setbar else _(u"否"),
            "isresize": _(u"是") if app.is_resize else _(u"否"),
            "is_already_online": app.is_already_online,
            "is_has": False,
            "user_app_id": "",
            "state": app.state,
            "app_visit_count": app_visit_count,
            "islapp": app.is_lapp,
        }
        # 判断用户是否添加了该应用
        user_app = UserApp.objects.filter(user=request.user, desk_app_type=0, app=app)
        if user_app:
            app_info["is_has"] = True
            app_info["user_app_id"] = user_app[0].id
        # 添加应用的用户
        all_user_app = UserApp.objects.filter(desk_app_type=0, app=app).values_list("user__username", flat=True)
        app_user = ", ".join(all_user_app)
        # app的版本信息
        app_version_list = []
        all_app_version = App_version.objects.filter(app=app).order_by("-pubdate")[0:5]
        for app_version in all_app_version:
            bug_list = []  # bug信息列表
            features_list = []  # features信息列表
            # 获取该版本的bug和feature信息
            app_features = app_version.versiondetail_set.all()
            for feature in app_features:
                if feature.bug:
                    bug_list.append(feature.bug.replace("\n", "<br/>"))
                if feature.features:
                    features_list.append(feature.features.replace("\n", "<br/>"))
            app_version_list.append(
                {
                    "version": app_version.version,
                    "bug": bug_list,
                    "features": features_list,
                    "publisher": app_version.publisher,
                    "pubdate": app_version.pubdate,
                }
            )
    except Exception as error:
        error_message = "%s, An error occurred while getting app detail page data, Error message:%s, App_id: %s" % (
            ConsoleErrorCodes.E1303102_MARKET_APP_DETAIL_QUERY_FAIL,
            error,
            app_id,
        )
        logger.error(error_message)
        app_info = {}  # 该应用基本信息
        app_version_list = []  # 应用版本信息
    ctx = {"app": app_info, "app_version": app_version_list, "app_user": app_user}
    return render(request, "desktop/market_app_detail.html", ctx)


def market_get_nearest_open_app(request):
    """
    获取用户最近打开的应用
    """
    user = request.user
    app_list = []
    # 获取最近打开的应用
    app_nearest_open = AppUseRecord.objects.filter(user=user).order_by("-use_time")
    app_nearest_open = app_nearest_open.values(
        "app__name", "app__name_en", "app__id", "app__code", "app__is_lapp", "use_time"
    )
    # 组装数据
    is_en = translation.get_language() == "en"

    app_code_set = set()
    for _app in app_nearest_open:
        if _app["app__code"] not in app_code_set:
            app_name = _app["app__name"]
            if is_en:
                app_name = _app["app__name_en"] or _app["app__name"]

            app_info = {
                "name": app_name,
                "code": _app["app__code"],
                "realid": _app["app__id"],
                "logo_url": get_app_logo_url(_app["app__code"]),
                "islapp": _app["app__is_lapp"],
            }
            app_list.append(app_info)
            app_code_set.add(_app["app__code"])
            # 只取前7个应用
            if len(app_code_set) >= 7:
                break
    ctx = {"app_list": app_list, "total": len(app_list)}
    return JsonResponse(ctx)
