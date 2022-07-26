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
from cachetools import TTLCache, cached
from django.conf import settings

from app.models import APP_LOGO_IMG_RELATED, App
from blueking.component.shortcuts import get_client_by_user
from common.log import logger


def get_app_logo_url(app_code):
    """
    通过app_code 获取 app 的logo (与开发者中心共用同一media资源)
    """
    try:
        app = App.objects.get(code=app_code)
        # PaaS3.0 的应用则直接读取 logo 字段中的值
        if app.is_in_paas3:
            return str(app.logo)
    except Exception as error:
        logger.error("An error occurred while getting app logo url: %s" % error)

    # 判断 以 app_code 命名的 logo 图片是否存在
    logo_name = "%s/%s.png" % (APP_LOGO_IMG_RELATED, app_code)
    return "%s%s" % (settings.MEDIA_URL, logo_name)


def _get_user_id(username):
    client = get_client_by_user(username)
    try:
        kwargs = {"exact_lookups": username, "lookup_field": "username", "fields": "username,id", "no_page": "true"}
        resp_json = client.usermgr.list_users(kwargs)
        if not resp_json.get("result"):
            logger.error("_get_user_id result=False: username=%s, resp=%s", username, resp_json)
            return None
        data = resp_json.get("data", [])
        if not data:
            logger.error("_get_user_id data empty: username=%s, resp=%s", username, resp_json)
            return None

        user_id = data[0]["id"]
    except Exception:
        logger.exception("query user profile fail!")
        return None

    return user_id


def _get_user_department_ids(username):
    client = get_client_by_user(username)
    try:
        kwargs = {
            "id": username,
            "with_family": "true",
        }
        resp_json = client.usermgr.list_profile_departments(kwargs)

        if not resp_json.get("result"):
            logger.error("_get_user_department_ids result=False: username=%s, resp=%s", username, resp_json)
            return None

        data = resp_json.get("data", [])

        department_ids = set()
        for d in data:
            department_ids.add(d["id"])

            if d.get("family"):
                for f in d.get("family"):
                    department_ids.add(f["id"])

        department_ids = list(department_ids)

    except Exception:
        logger.exception("query user departments fail!")
        return None

    return department_ids


@cached(cache=TTLCache(maxsize=1024, ttl=60))
def get_visiable_labels(username):
    user_id = _get_user_id(username)
    department_ids = _get_user_department_ids(username)

    if not (user_id and department_ids):
        return []

    # username => u:username
    visiable_labels = ["u:%s" % user_id]
    visiable_labels.extend(["d:%s" % d for d in department_ids])

    # for query term: ,u:1,   ,d:100,   ,d:200,   ,u:2,
    # in database ,u:1,d:111,d:222,u:2,
    visiable_labels = [",%s," % v for v in visiable_labels]

    return visiable_labels
