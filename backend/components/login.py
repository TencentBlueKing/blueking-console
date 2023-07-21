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
from components.esb import _call_esb_api
from components.http import http_get


def is_login(bk_token):
    """
    校验登录态
    """
    path = '/api/c/compapi/v2/bk_login/is_login/'
    _, code, message, data = _call_esb_api(http_get, path, {"bk_token": bk_token})
    return code, message, data


def get_user(bk_token):
    """
    校验登录态
    """
    path = '/api/c/compapi/v2/bk_login/get_user/'
    _, code, message, data = _call_esb_api(http_get, path, {"bk_token": bk_token})
    return code, message, data
