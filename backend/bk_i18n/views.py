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
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.translation import LANGUAGE_SESSION_KEY, check_for_language

from bk_i18n.constants import DJANGO_LANG_TO_BK_LANG, TIME_ZONE_LIST
from components import usermgr


def _get_response(request):
    next = request.POST.get("next", request.GET.get("next"))
    if not is_safe_url(next, request.get_host()):
        next = request.META.get("HTTP_REFERER")
        if not is_safe_url(next, request.get_host()):
            next = "/"
    return HttpResponseRedirect(next)


def set_language(request):
    response = _get_response(request)
    if request.method == "POST":
        language = request.POST.get("language", None)
        if language and check_for_language(language):
            # 调用login接口设置
            username = request.user.username
            is_success, message = usermgr.reset_user_i18n_language(username, DJANGO_LANG_TO_BK_LANG[language])
            if is_success:
                request.session[LANGUAGE_SESSION_KEY] = language
                response.set_cookie(
                    settings.LANGUAGE_COOKIE_NAME,
                    DJANGO_LANG_TO_BK_LANG[language],
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                )
    return response


def set_timezone(request):
    response = _get_response(request)
    if request.method == "POST":
        timezone = request.POST.get("timezone", None)
        if timezone and timezone in TIME_ZONE_LIST:
            # 调用login接口设置
            username = request.user.username
            is_success, message = usermgr.reset_user_i18n_timezone(username, timezone)
            if is_success:
                request.session[settings.TIMEZONE_SESSION_KEY] = timezone

    return response
