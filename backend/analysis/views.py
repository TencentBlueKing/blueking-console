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

from django.db.models import F

from analysis.models import AppLiveness, AppOnlineTimeRecord, AppUseRecord
from analysis.utils import get_request_param, get_source_ip, response_json_or_jsonp
from app.models import App
from common.log import logger


def app_record_by_user(request, app_id_or_code):
    """
    app使用信息记录
    app_id: app的真实id
    POST 请求，参数为app_id
    GET 请求，参数为app_code，且返回为jsonp
    """
    request_param = get_request_param(request)
    callback = request_param.get("callback", "")
    try:
        if request.method == "GET":
            app_id = App.objects.get(code=app_id_or_code).id
        else:
            app_id = int(app_id_or_code)
    except Exception:
        app_id = ""

    # 记录app的使用信息
    user = request.user
    access_host = request.get_host()
    source_ip = get_source_ip(request)

    is_success = AppUseRecord.objects.save_app_use_record(user, app_id, access_host, source_ip)
    return response_json_or_jsonp({"result": is_success}, callback)


def app_liveness_save(request):
    """
    保存 APP 点击量
    GET 请求返回为jsonp
    """
    request_param = get_request_param(request)
    callback = request_param.get("callback", "")
    # 接口参数
    app_msg = request_param.get("app_msg", "{}")
    try:
        app_msg = json.loads(app_msg)
    except Exception:
        logger.exception("load param app_msg json fail")
        return response_json_or_jsonp({"result": False}, callback)

    user = request.user
    # 记录app的使用信息
    access_host = request.get_host()
    source_ip = get_source_ip(request)

    # 遍历 上报的 app
    for _app in app_msg:
        try:
            app = App.objects.filter(code=_app)
            app = app[0] if app else None
            if not app:
                continue

            app_data = AppLiveness.objects.filter(app=app, user=user)
            # 判断是否有今日的数据
            if app_data:
                # 当日数据累加
                app_data.update(hits=F("hits") + int(app_msg[_app]))
            else:
                # 创建新的记录
                AppLiveness(
                    app=app, user=user, hits=int(app_msg[_app]), access_host=access_host, source_ip=source_ip
                ).save()
        except Exception as error:
            logger.error("An error occurred while saving App liveness: %s" % error)
    return response_json_or_jsonp({"result": True}, callback)


def app_online_time_save(request):
    """
    保存app 在线时长数据
    GET 请求返回为jsonp
    """
    request_param = get_request_param(request)
    callback = request_param.get("callback", "")
    # 接口参数
    app_msg = request_param.get("app_msg", "{}")
    # {'workbench':{'2013-09-02': 55555, '2012-09-08': 9999}, 'app_one':{'2013-09-02': 55555, '2012-09-08': 9999}}
    try:
        app_msg = json.loads(app_msg)
    except Exception:
        logger.exception("load param app_msg json fail")
        return response_json_or_jsonp({"result": False}, callback)

    # 记录app的使用信息
    user = request.user
    access_host = request.get_host()
    source_ip = get_source_ip(request)

    # 遍历 上报的 app
    for _app, _app_data in list(app_msg.items()):
        try:
            # 0:平台及系统应用, 1:普通应用
            record_type = 0 if _app == "workbench" or not _app else 1
            time_online = sum([float(i) / 1000 for i in list(_app_data.values()) if i])
            if time_online:
                # 创建新的记录
                AppOnlineTimeRecord(
                    app_code=_app,
                    record_type=record_type,
                    user=user,
                    online_time=time_online,
                    access_host=access_host,
                    source_ip=source_ip,
                ).save()
        except Exception as error:
            logger.error("An error occurred while saving App online time data:%s" % error)
    return response_json_or_jsonp({"result": True}, callback)
