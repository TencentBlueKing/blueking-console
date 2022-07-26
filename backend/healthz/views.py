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

import os
from builtins import str

import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _

from account.decorators import login_exempt
from common.exceptions import ConsoleErrorCodes
from common.license_utils import check_license

# ====================  helpers =========================

CONSOLE_MODULE_CODE = "1303000"


def _gen_json_response(ok, code, message, data):
    """
    ok: True/False
    code:  平台 1303000 / 模块 1303100 / 具体错误  1303105
    message: 报错信息
    data: dict, 内容自定义
    """
    return JsonResponse({"ok": ok, "code:": code, "message": message, "data": data}, status=200)


def _gen_success_json_response(data):
    """
    成功
    """
    return _gen_json_response(ok=True, code=CONSOLE_MODULE_CODE, message="OK", data=data)


def _gen_fail_json_response(code, message, data):
    """
    失败
    """
    return _gen_json_response(ok=False, code=code, message=message, data=data)


# ====================  check =========================


def _check_settings():
    """
    check settings, 注意不暴露密码等敏感信息
    """
    # check settings, 注意不暴露密码等敏感信息
    try:
        settings.ESB_TOKEN
        {
            "debug": settings.DEBUG,
            "env": os.getenv("BK_ENV", "unknow"),
            "paas_domain": settings.PAAS_DOMAIN,
            "cookie_domain": settings.BK_COOKIE_DOMAIN,
            "host_login": settings.LOGIN_HOST,
            "mysql": {
                "host": settings.DATABASES.get("default", {}).get("HOST"),
                "port": settings.DATABASES.get("default", {}).get("PORT"),
                "user": settings.DATABASES.get("default", {}).get("USER"),
                "database": settings.DATABASES.get("default", {}).get("NAME"),
            },
        }
    except Exception as e:
        return False, _(u"配置文件不正确, 缺失对应配置: %s") % str(e), ConsoleErrorCodes.E1303001_BASE_SETTINGS_ERROR

    return True, "ok", 0


def _check_database():
    try:
        from desktop.models import Wallpaper

        objs = Wallpaper.objects.all()
        [o.name for o in objs]
    except Exception as e:
        return False, _(u"数据库连接存在问题: %s") % str(e), ConsoleErrorCodes.E1303002_BASE_DATABASE_ERROR

    return True, "ok", 0


def _check_hosts():
    # check hosts
    # 不检查cc/jos, 因为不是强依赖只是用来展示, 用户浏览器能访问通即可, paas所在机器不需要

    # login 只检查 healthz api，否则自定义登录会重定向
    login_url = "%s/healthz/" % settings.LOGIN_HOST
    hosts = {
        "login_url": login_url,
    }
    for name, host in hosts.items():
        try:
            if not host.startswith("http"):
                host = "http://%s" % host
            requests.get(host, timeout=10)
        except Exception as e:
            return (
                False,
                _(u"第三方依赖连接超时: name=%(name)s, host=%(host)s,  error=%(error)s")
                % {"name": name, "host": host, "error": str(e)},
                ConsoleErrorCodes.E1303003_BASE_HTTP_DEPENDENCE_ERROR,
            )

    return True, "ok", 0


def _warning_database_bksuite():
    if 'bksuite' not in settings.DATABASES:
        return {"database bksuite": "not set"}

    data = {}
    try:
        import django.db

        with django.db.connections["bksuite"].cursor() as c:
            c.execute("SELECT 0")
    except django.db.Error as e:
        msg = _(u"%(ecode)s Bksuite数据库连接存在问题 %(error)s; 不影响使用, 但[蓝鲸智云 - 开发者中心 - 版本信息]无法正常展示") % {
            "ecode": ConsoleErrorCodes.E1303004_BASE_BKSUITE_DATABASE_ERROR,
            "error": str(e),
        }
        data["database bksuite"] = msg
    else:
        data["database bksuite"] = "ok"

    return data


def _warning_license():
    # 未开启证书服务
    if not settings.IS_CERTIFICATE_SVC_ENABLED:
        return {"license": "disabled"}

    data = {}
    # check license
    is_license_ok, message, valid_start_time, valid_end_time = check_license()
    if not is_license_ok:
        data["license"] = _(u"%(error_code)s 企业证书无效：%(error)s; 只影响桌面版本信息的展示") % {
            "error_code": ConsoleErrorCodes.E1303005_BASE_LICENSE_ERROR,
            "error": message,
        }
    else:
        data["license"] = "ok"

    return data


@login_exempt
def healthz(request):
    """
    health check
    """
    data = {}

    # 强依赖
    _check_funcs = [
        ("settings", _check_settings),
        ("database", _check_database),
        ("hosts", _check_hosts),
    ]
    for name, func in _check_funcs:
        is_health, message, code = func()
        if is_health:
            data[name] = "ok"
        else:
            return _gen_fail_json_response(code=code, message=message, data={})

    # 弱依赖, 有损服务
    _warnning_funcs = [_warning_database_bksuite, _warning_license]
    for func in _warnning_funcs:
        _data = func()
        data.update(_data)

    return _gen_success_json_response(data)


@login_exempt
def ping(request):
    return HttpResponse("pong", content_type="text/plain")
