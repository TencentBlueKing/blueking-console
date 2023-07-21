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
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.utils import translation

from account.exceptions import AccessPermissionDenied
from bk_i18n.constants import BK_LANG_TO_DJANGO_LANG
from common.log import logger
from components.login import get_user, is_login


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

    if settings.LOGIN_DOMAIN:
        BK_LOGIN_URL = "http://%s/login/" % settings.LOGIN_DOMAIN
    else:
        BK_LOGIN_URL = "/login/"

    # 蓝鲸统一登录约定的错误码, 表示用户认证成功，但用户无应用访问权限
    ACCESS_PERMISSION_DENIED_CODE = 1302403

    def is_bk_token_valid(self, request):
        """验证用户登录态."""
        bk_token = request.COOKIES.get(settings.BK_COOKIE_NAME, None)
        if not bk_token:
            return False, None
        ret, data = self.verify_bk_login(bk_token)
        # bk_token 无效
        if not ret:
            return False, None
        # 检查用户是否存在用户表中
        username = data.get("bk_username", "")
        user_model = get_user_model()
        try:
            user = user_model._default_manager.get_by_natural_key(username)
            is_created_user = False
        except user_model.DoesNotExist:
            user = user_model.objects.create_user(username)
            is_created_user = True
        finally:
            try:
                ret, data = self.get_bk_user_info(bk_token)
                # 若获取用户信息失败，则用户可登录，但用户其他信息为空
                user.chname = data.get("chname", "")

                # 用户隐私信息置空，需要的时候直接从用户管理 API 中获取
                user.company = data.get("company", "")
                user.qq = ""
                user.phone = ""
                user.email = ""
                user.role = ""

                # 仅新用户从用户管理同步权限
                # 用户创建后直接在桌面管理用户是否能进入到 admin 页面的权限
                if is_created_user:
                    role = data.get("bk_role", "")
                    is_superuser = True if role == 1 else False
                    user.is_superuser = is_superuser
                    user.is_staff = is_superuser
                user.save()

                # 设置timezone session
                request.session[settings.TIMEZONE_SESSION_KEY] = data.get("time_zone")
                # 设置language session
                request.session[translation.LANGUAGE_SESSION_KEY] = BK_LANG_TO_DJANGO_LANG[data.get("language")]
            except Exception as e:
                logger.error("Get and record user information failed：%s" % e)
        return True, user

    def verify_bk_login(self, bk_token):
        """请求平台接口验证登录是否失效"""
        code, message, data = is_login(bk_token)
        if code == 0:
            return True, data

        if code == self.ACCESS_PERMISSION_DENIED_CODE:
            logger.info("No access permission: %s" % message)
            raise AccessPermissionDenied(message)

        logger.error("Verification of user login token is invalid, code: %s,  message: %s" % (code, message))
        return False, {}

    def get_bk_user_info(self, bk_token):
        """请求平台接口获取用户信息"""
        code, message, data = get_user(bk_token)
        if code == 0:
            return True, data

        if code == self.ACCESS_PERMISSION_DENIED_CODE:
            logger.info("No access permission: %s" % message)
            raise AccessPermissionDenied(message)

        logger.error(
            "Get user information from the request platform interface failed, code: %s,  message: %s" % (code, message)
        )
        return False, {}

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
        if is_login:
            # 登录
            callback = self.build_callback_url(request, self.BK_LOGIN_URL)
        else:
            # 登出
            login_url = "%s?%s" % (self.BK_LOGIN_URL, "is_from_logout=1")
            callback = self.http_referer(request)
        return redirect_to_login(callback, login_url, settings.REDIRECT_FIELD_NAME)

    def redirect_login(self, request):
        """
        重定向到登录页面.
        登录态验证不通过时调用
        """
        # ajax跳401
        if request.is_ajax():
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
