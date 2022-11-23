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

usermgr api
"""
from __future__ import absolute_import

from .esb import _call_esb_api
from .http import http_post


def batch_query_users(username_list=[], is_complete=False):
    """
    批量获取用户，可以获取所有
    """
    path = "/api/c/compapi/v1/usermanage/login/profile/query/"

    data = {
        "username_list": username_list,
        "is_complete": is_complete,
    }

    ok, _, message, _data = _call_esb_api(http_post, path, data)
    return ok, message, _data


def upsert_user(username, **kwargs):
    """
    创建或更新用户
    主要用于ee_login，企业第三方应用某些情况下需要支持将用户存储到用户管理
    """
    path = "/api/c/compapi/v1/usermanage/login/profile/"

    data = {
        "username": username,
    }
    data.update(kwargs)
    # ok, _, message, _data = _call_usermgr_api(http_post, url, data)
    ok, _, message, _data = _call_esb_api(http_post, path, data)
    return ok, message, _data
