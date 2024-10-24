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
import pytz
from django.conf import settings
from django.utils import timezone, translation
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tzname = request.session.get(settings.TIMEZONE_SESSION_KEY)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()


class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        language = request.session.get(settings.LANGUAGE_SESSION_KEY)
        if language:
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
