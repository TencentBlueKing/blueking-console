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
from django.conf import settings
from django.contrib.auth import get_user_model

from common.http import http_get
from common.log import logger


def _get_users_from_login_service(bk_token):
    """
    获取所有用户的信息
    """
    param = {"bk_token": bk_token}
    if settings.LOGIN_DOMAIN:
        get_user_url = "http://%s/login/accounts/get_all_user/" % settings.LOGIN_DOMAIN
    else:
        get_user_url = "%s/login/accounts/get_all_user/" % settings.LOGIN_HOST

    result, resp = http_get(get_user_url, param)
    resp = resp if result and resp else {}
    ret = resp.get("result", False) if result and resp else False
    # 获取用户信息失败
    if not ret:
        logger.error(u"Get user information from the request platform interface failed：%s" % resp.get("message", ""))
        return False, []
    return True, resp.get("data", [])


def get_users(request):
    # 用户信息从统一登录接口获取
    bk_token = request.COOKIES.get(settings.BK_COOKIE_NAME, None)
    res, users = _get_users_from_login_service(bk_token)
    # 接口返回出错则直接从数据库获取
    if not res:
        # 获取所有的用户信息
        user_model = get_user_model()
        users = user_model.objects.all().values("username")
    return users
