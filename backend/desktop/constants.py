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
from builtins import zip

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common.constants import enum

# 文件夹图标默认图片
DEFALUT_FOLDER_ICO = settings.STATIC_URL + "img/base_ui/folder_default.png"

# 应用市场左侧导航类别
MarketNavEnum = enum(
    CREATOR=0,
    APPTAG=1,
)

MARKET_NAV_CHOICES = [
    (MarketNavEnum.CREATOR, _(u"应用创建者")),
    (MarketNavEnum.APPTAG, _(u"应用分类")),
]


# 应用按创建者分类
AppCreatorTagEnum = enum(
    EEUSER=1,
    BLUEKING=2,
    JIAWEI=3,
    QIZHI=4,
    HAOXI=5,
    HONGYUCHUANGZHANG=6,
    OTHER=99,
)

CREATOR_TAG_CHOICES = [
    (AppCreatorTagEnum.EEUSER, _(u"用户自建")),
    (AppCreatorTagEnum.BLUEKING, _(u"蓝鲸智云")),
    (AppCreatorTagEnum.JIAWEI, _(u"嘉为蓝鲸")),
    (AppCreatorTagEnum.QIZHI, _(u"齐治科技")),
    (AppCreatorTagEnum.HAOXI, _(u"皓西科技")),
    (AppCreatorTagEnum.HONGYUCHUANGZHANG, _(u"红雨创展")),
    (AppCreatorTagEnum.OTHER, _(u"其它")),
]

CREATOR_TAG_DICT = dict(CREATOR_TAG_CHOICES)

# 蓝鲸和蓝鲸服务商创建者列表
BK_CREATOR_TAG_LIST, BK_CREATOR_TAG_STR_LIST = list(zip(*CREATOR_TAG_CHOICES[1:-1]))
