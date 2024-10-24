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
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from app.models import App
from common.log import logger


def login_exempt(view_func):
    """
    登录豁免,被此装饰器修饰的action可以不校验登录
    """

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.login_exempt = True
    return wraps(view_func)(wrapped_view)


def is_superuser_perm(view_func):
    """
    检查是否管理员
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return render(request, "403.html")

    return _wrapped_view


def verfy_request_header(view_func):
    """
    验证HTTP请求头
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        x_app_token = request.META.get("HTTP_X_APP_TOKEN")
        x_app_code = request.META.get("HTTP_X_APP_ID")
        if not all([x_app_token, x_app_code]):
            return JsonResponse(
                {
                    "result": False,
                    "code": "1100",
                    "message": _(u"请求头缺少参数:HTTP_X_APP_ID / HTTP_X_APP_TOKEN"),
                    "data": {},
                }
            )
        try:
            # ESB 的token 存放在settings中
            if x_app_code == "esb" and x_app_token == settings.ESB_TOKEN:
                return view_func(request, *args, **kwargs)

            app = App.objects.get(code=x_app_code)
            app_token = app.auth_token
            if not x_app_token == app_token:
                return JsonResponse(
                    {
                        "result": False,
                        "code": "1101",
                        "message": _(u"参数不匹配:HTTP_X_APP_ID / HTTP_X_APP_TOKEN"),
                        "data": {},
                    }
                )
        except Exception as e:
            logger.exception("Verification of HTTP request header is abnormal:%s" % e)
            return JsonResponse({"result": False, "code": "1102", "message": _(u"参数不合法:HTTP_X_APP_ID"), "data": {}})

        return view_func(request, *args, **kwargs)

    return _wrapped_view
