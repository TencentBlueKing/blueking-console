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

from __future__ import unicode_literals


def enum(**enums):
    return type("Enum", (), enums)


ConsoleErrorCodes = enum(
    E1303000_DEFAULT_CODE=1303000,
    E1303001_BASE_SETTINGS_ERROR=1303001,
    E1303002_BASE_DATABASE_ERROR=1303002,
    E1303003_BASE_HTTP_DEPENDENCE_ERROR=1303003,
    E1303004_BASE_BKSUITE_DATABASE_ERROR=1303004,
    E1303005_BASE_LICENSE_ERROR=1303005,
    # 加载桌面应用错误
    E1303100_DESKTOP_USER_APP_LOAD_ERROR=1303100,
    # 应用市场查询应用失败
    E1303101_MARKET_APP_QUERY_FAIL=1303101,
    # 应用市场应用详情查询失败
    E1303102_MARKET_APP_DETAIL_QUERY_FAIL=1303102,
    # 请求微信GET接口出错
    E1303200_WEIXIN_HTTP_GET_REQUEST_ERROR=1303200,
    # 请求微信POST接口出错
    E1303201_WEIXIN_HTTP_POST_REQUEST_ERROR=1303201,
    # 微信公众号推送事件响应出错
    E1303202_WEIXIN_MP_EVENT_PUSH_RESPONSE_ERROR=1303202,
)
