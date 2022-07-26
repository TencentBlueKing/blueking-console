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
import json
import re

from django.http import HttpResponse, JsonResponse

CALLBACK_PATTERN = re.compile(r"^[0-9a-zA-Z_.]+$")


def response_json_or_jsonp(result, callback):
    """
    返回支持jsonp跨域请求的response对象
    result: json字典
    callback: json返回函数，必须使用callback(data),返回json串
    """
    if not callback:
        # 非 jsonp，普通json返回
        return JsonResponse(result)
    # 防止jsonp xss攻击
    if not CALLBACK_PATTERN.match(callback):
        # callback 不符合 字符+数字+下划线+点号 则直接用json返回，防止<script>等等攻击
        return JsonResponse(result)
    # jsonp的跨域调用方式
    response = HttpResponse(content_type="application/javascript")
    response.content = "%s(%s)" % (callback, json.dumps(result))
    return response


def get_request_param(request):
    if request.method == "GET":
        request_param = request.GET
    else:
        request_param = request.POST
    return request_param


def get_source_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        source_ip = x_forwarded_for.split(",")[0]
    else:
        source_ip = request.META.get("REMOTE_ADDR", "unknown")
    return source_ip
