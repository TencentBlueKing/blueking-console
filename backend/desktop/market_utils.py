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

from django.conf import settings

from apigw.client import BkUserAPIClient
from app.models import App, AppTags
from common.constants import AppTenantMode
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


def get_creator_display_names(apps):
    """获取应用创建者的展示名称，全租户应用则直接展示租户 ID

    :param apps: 应用列表
    :return: 应用 ID 和 应用创建者展示名称的字典
    """
    # 未开启多租户，则展示 DB 中存储的信息
    if not settings.ENABLE_MULTI_TENANT_MODE:
        return {app.id: app.creater_display for app in apps}

    display_mapping = {}

    # 全租户应用，展示名为租户 ID，或配置的固定值
    global_apps = apps.filter(app_tenant_mode=AppTenantMode.GLOBAL)
    display_mapping.update({app.id: settings.GLOBAL_TENANT_APP_DEVELOPER or app.tenant_id for app in global_apps})

    # 非全租户应用，按租户获取应用创建者的展示名称
    normal_tenant_ids = (
        apps.exclude(app_tenant_mode=AppTenantMode.GLOBAL).values_list("tenant_id", flat=True).distinct()
    )
    for tenant_id in normal_tenant_ids:
        tenant_apps = apps.filter(tenant_id=tenant_id)
        tenant_creators = {app.creater for app in tenant_apps}
        try:
            client = BkUserAPIClient(tenant_id)
            user_display_map = client.batch_query_user_display_info(list(tenant_creators))

            # 如果没有查询到用户的 display name，则使用原来的名称
            for app in tenant_apps:
                display_mapping[app.id] = user_display_map.get(app.creater, app.creater_display)
        except Exception:
            logger.exception("Error in querying user display name for tenant(%s)", tenant_id)
            continue

    return display_mapping


def get_single_creator_display_name(app: App) -> str:
    """获取单个应用创建者的展示名称

    :param app: 应用实例
    :return: 应用创建者展示名称
    """
    # 未开启多租户，则展示 DB 中存储的信息
    if not settings.ENABLE_MULTI_TENANT_MODE:
        return app.creater_display

    # 全租户应用，展示名为租户 ID，或配置的固定值
    if app.app_tenant_mode == AppTenantMode.GLOBAL:
        return settings.GLOBAL_TENANT_APP_DEVELOPER or app.tenant_id

    try:
        client = BkUserAPIClient(app.tenant_id)
        user_display_map = client.batch_query_user_display_info([app.creater])
        return user_display_map.get(app.creater, app.creater_display)
    except Exception:
        logger.exception("Error in querying user display name for app(%s)", app.id)
        # 异常时返回原始用户名
        return app.creater_display
