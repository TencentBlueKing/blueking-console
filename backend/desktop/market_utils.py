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
from app.models import App, AppTags
from desktop.constants import CREATOR_TAG_CHOICES, MarketNavEnum
from desktop.models import UserSettings


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
