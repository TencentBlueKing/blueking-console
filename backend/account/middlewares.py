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

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.middleware.csrf import get_token as get_csrf_token
from django.utils.deprecation import MiddlewareMixin

from account.accounts import Account


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """设置user"""
        # 静态资源不做登录态设置
        full_path = request.get_full_path()
        if full_path.startswith(settings.STATIC_URL) or full_path == "/robots.txt":
            return None

        user = authenticate(request=request)
        request.user = user or AnonymousUser()

    def process_view(self, request, view, args, kwargs):
        # 静态资源不做登录态验证
        full_path = request.get_full_path()
        if full_path.startswith(settings.STATIC_URL) or full_path == "/robots.txt":
            return None

        if full_path in [settings.SITE_URL + "jsi18n/i18n/", "/jsi18n/i18n/"]:
            return None

        if getattr(view, "login_exempt", False):
            return None

        if not isinstance(request.user, AnonymousUser):
            get_csrf_token(request)
            return None

        account = Account()
        return account.redirect_login(request)
