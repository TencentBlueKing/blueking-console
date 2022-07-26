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
import pytz

from common.constants import enum

LanguageEnum = enum(ZH_CN="zh-cn", EN="en")

DJANGO_LANG_TO_BK_LANG = {"zh-hans": LanguageEnum.ZH_CN, "en": LanguageEnum.EN}

BK_LANG_TO_DJANGO_LANG = {v: k for k, v in DJANGO_LANG_TO_BK_LANG.items()}

TIME_ZONE_LIST = pytz.common_timezones
