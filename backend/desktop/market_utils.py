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
import logging
from collections import defaultdict

from django.conf import settings

from apigw.client import BkUserAPIClient
from app.models import App, AppTags
from common.constants import OP_TYPE_TENANT_ID, AppTenantMode
from desktop.constants import CREATOR_TAG_CHOICES, MarketNavEnum
from desktop.models import UserSettings

logger = logging.getLogger("root")


def _get_app_creator_list():
    """
    获取应用创建者分类
    """
    # 默认有分类：蓝鲸智云，用户自建，其它
    creator_tag_list = CREATOR_TAG_CHOICES[:2]
    # 需要检查是否存在应用，否则不展示的分类
    for i in CREATOR_TAG_CHOICES[2:-1]:
        if App.objects.filter(creater=i[1]).exists():
            creator_tag_list.append(i)
    creator_tag_list.append(CREATOR_TAG_CHOICES[-1])
    return creator_tag_list


def get_market_nav_and_tag_list(username):
    """
    根据用户配置，获取分类列表
    """
    market_nav = UserSettings.objects.get_user_market_nav(username)
    # 应用分类
    if market_nav == MarketNavEnum.CREATOR:
        return market_nav, _get_app_creator_list()
    return market_nav, AppTags.objects.get_all_tags_with_100id()


def get_creator_display(apps, user_tenant_id):
    """
    获取应用创建者展示名称（支持批量查询和单个查询）
    :param apps: 可接受类型：
                - 单个App实例
                - App查询集/列表
    :param user_tenant_id: 用户租户ID
    :return: 单应用模式返回字符串，否则返回{应用ID: 展示名称}字典
    """
    # 统一输入格式处理
    if isinstance(apps, App):
        app_list = [apps]
    else:
        app_list = apps

    display_mapping = {}
    tenant_apps_map = defaultdict(list)

    # 第一轮遍历：处理全租户应用 + 分组非全租户应用
    for app in app_list:
        # 全租户应用，且当前用户不属于运营租户，则不需要查询应用创建者的展示名称
        # 展示应用所属租户 ID 或者系统的一个默认配置值
        if app.app_tenant_mode == AppTenantMode.GLOBAL and user_tenant_id != OP_TYPE_TENANT_ID:
            display_name = settings.GLOBAL_TENANT_APP_DEVELOPER or app.tenant_id
            display_mapping[app.id] = display_name
        else:
            tenant_apps_map[app.tenant_id].append(app)

    # 第二轮遍历：批量处理非全租户应用
    for tenant_id, tenant_apps in tenant_apps_map.items():
        creators = {app.creater for app in tenant_apps}

        try:
            client = BkUserAPIClient(tenant_id)
            user_display_map = client.batch_query_user_display_info(list(creators))

            for app in tenant_apps:
                display_mapping[app.id] = user_display_map.get(app.creater, app.creater_display)
        except Exception:
            logger.exception("查询租户(%s)用户显示名称失败", tenant_id)
            for app in tenant_apps:
                display_mapping[app.id] = app.creater_display

    return display_mapping
