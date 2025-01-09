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
账号体系相关的基类Account.
"""
from builtins import object
from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render

from account.exceptions import AccessPermissionDenied
from apigw.client import BkLoginClient
from apigw.exceptions import BkLoginNoAccessPermission
from bk_i18n.constants import BK_LANG_TO_DJANGO_LANG
from common.log import logger


class AccountSingleton(object):
    """
    单例基类.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class Account(AccountSingleton):
    """
    账号体系相关的基类Account.
    提供通用的账号功能
    """

    # 本地开发时会配置 LOGIN_DOMAIN
    if settings.LOGIN_DOMAIN:
        BK_LOGIN_URL = f"{settings.HTTP_SCHEMA}://{settings.LOGIN_DOMAIN}/login/"
    else:
        # 线上 LOGIN_DOMAIN 为空
        BK_LOGIN_URL = "/login/"

    def is_bk_token_valid(self, request):
        """验证用户登录态."""
        bk_token = request.COOKIES.get(settings.BK_COOKIE_NAME, None)
        if not bk_token:
            return False, None

        # 校验并获取用户信息
        try:
            data = BkLoginClient().get_user(bk_token)
        except BkLoginNoAccessPermission as e:
            raise AccessPermissionDenied(e)
        except Exception:
            return False, None

        # 检查用户是否存在用户表中
        username = data.get("bk_username", "")
        user_model = get_user_model()
        try:
            user = user_model._default_manager.get_by_natural_key(username)
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(username)
        finally:
            try:
                user.chname = data.get("display_name", username)
                # 用户隐私信息置空，需要的时候直接从用户管理 API 中获取
                user.company = data.get("company", "")
                user.qq = ""
                user.phone = ""
                user.email = ""
                user.role = ""
                user.save()

                # 设置timezone session
                request.session[settings.TIMEZONE_SESSION_KEY] = data.get("time_zone")
                # 设置language session
                request.session[settings.LANGUAGE_SESSION_KEY] = BK_LANG_TO_DJANGO_LANG[data.get("language")]
            except Exception as e:
                logger.error("Get and record user information failed：%s" % e)
        return True, user

    def build_callback_url(self, request, jump_url):
        callback = request.build_absolute_uri()
        login_scheme, login_netloc = urlparse(jump_url)[:2]
        current_scheme, current_netloc = urlparse(callback)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            callback = request.get_full_path()
        return callback

    def _redirect_login(self, request, is_login=True):
        """
        跳转平台进行登录
        """
        login_url = self.BK_LOGIN_URL
        redirect_field_name = settings.REDIRECT_FIELD_NAME
        # 所有页面重新登录成功后都是回调到桌面首页
        redirect_url = settings.SITE_URL

        query_params = {redirect_field_name: redirect_url}
        # 退出登录需要添加指定的参数
        if not is_login:
            query_params["is_from_logout"] = 1

        full_login_url = f"{login_url}?{urlencode(query_params)}"
        # 由于页面都是通过 IFrame 嵌入，所以需要刷新 parent 的页面，否则页面会一直重定向
        return render(request, "redirect_to_login.html", {"login_url": full_login_url})

    def _is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def redirect_login(self, request):
        """
        重定向到登录页面.
        登录态验证不通过时调用
        """
        # ajax跳401
        if self._is_ajax(request=request):
            return HttpResponse(status=401)
        # 非ajax请求 跳转至平台登录
        return self._redirect_login(request)

    def http_referer(self, request):
        """
        获取 HTTP_REFERER 头，得到登出后要重新登录跳转的url
        """
        if "HTTP_REFERER" in request.META:
            http_referer = request.META["HTTP_REFERER"]
        else:
            http_referer = settings.LOGIN_REDIRECT_URL
        return http_referer

    def logout(self, request):
        """登出并重定向到登录页面."""
        auth_logout(request)
        return self._redirect_login(request, False)
