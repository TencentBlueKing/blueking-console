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
import logging

from bkapi_client_core.exceptions import APIGatewayResponseError, JSONResponseError, ResponseError
from django.conf import settings

from apigw.bk_login import Client as LoginClient
from apigw.bk_user import Client as UserClient
from apigw.bk_user_web import Client as UserWebClient
from apigw.exceptions import BkLoginGatewayServiceError, BkLoginNoAccessPermission

logger = logging.getLogger(__name__)


class BkLoginClient:
    def __init__(self):
        client = LoginClient(endpoint=settings.BK_API_URL_TMPL, stage="prod")
        client.update_bkapi_authorization(
            bk_app_code="bk_paas",
            bk_app_secret=settings.BK_APP_SECRET,
        )
        client.update_headers(self._prepare_headers())
        self.client = client.api

    def _prepare_headers(self) -> dict:
        return {
            # 调用全租户网关时，网关会强制要求传递 X-Bk-Tenant-Id, 但不会实际校验值的有效性, 统一传 default
            "X-Bk-Tenant-Id": "default",
        }

    def get_user(self, bk_token: str) -> dict:
        try:
            resp = self.client.get_bk_token_userinfo(params={"bk_token": bk_token})
        except (APIGatewayResponseError, ResponseError) as e:
            logger.exception(f"call bk login api error, detail: {e}")
            # 用户无权限时需要单独处理
            if e.response.status_code == 403:
                raise BkLoginNoAccessPermission(e.response.json()["error"]["message"])
            raise BkLoginGatewayServiceError("call bk login api error")

        return resp["data"]


class BkUserAPIClient:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        client = UserClient(endpoint=settings.BK_API_URL_TMPL, stage="prod")
        authorization = {
            "bk_app_code": "bk_paas",
            "bk_app_secret": settings.BK_APP_SECRET,
        }
        client.update_bkapi_authorization(**authorization)
        client.update_headers(self._prepare_headers())
        self.client = client.api

    def _prepare_headers(self) -> dict:
        return {
            # 只能查询 tenant_id 租户下的用户信息
            "X-Bk-Tenant-Id": self.tenant_id,
        }

    def batch_query_user_display_info(self, username_list: list) -> dict:
        """批量查询用户展示信息

        :param username_list: 用户名列表
        """
        bk_usernames = ",".join(username_list)
        try:
            resp = self.client.batch_query_user_display_info(params={"bk_usernames": bk_usernames})
        except (APIGatewayResponseError, ResponseError) as e:
            logger.exception(f"call bk user api batch_query_user_display_info error, detail: {e}")
            raise BkLoginGatewayServiceError("call bk user api batch_query_user_display_info error")

        user_data = resp.get("data", [])
        return {
            user["bk_username"]: user["display_name"]
            for user in user_data
            if user.get("bk_username") and user.get("display_name")
        }

    def get_user_department_ids(self, username: str) -> list:
        """获取用户部门 ID 列表，包含所有父部门

        :param username: 用户名
        """
        try:
            # 包括所有祖先部门
            resp = self.client.list_user_department(
                path_params={"bk_username": username}, params={"with_ancestors": True}
            )
        except (APIGatewayResponseError, ResponseError) as e:
            logger.exception(f"call bk user api list_user_department error, detail: {e}")
            raise BkLoginGatewayServiceError("call bk user api list_user_department error")

        data = resp.get("data", [])
        department_ids = set()
        for d in data:
            department_ids.add(d["id"])

            if d.get("family"):
                for f in d.get("ancestors"):
                    department_ids.add(f["id"])

        department_ids = list(department_ids)
        return department_ids


class BkUserWebAPIClient:
    def __init__(self, tenant_id: str, bk_token: str):
        self.tenant_id = tenant_id
        client = UserWebClient(endpoint=settings.BK_API_URL_TMPL, stage="prod")
        authorization = {
            "bk_app_code": "bk_paas",
            "bk_app_secret": settings.BK_APP_SECRET,
            settings.BK_COOKIE_NAME: bk_token,
        }
        client.update_bkapi_authorization(**authorization)
        client.update_headers(self._prepare_headers())
        self.client = client.api

    def _prepare_headers(self) -> dict:
        return {
            # 只能查询 tenant_id 租户下的用户信息
            "X-Bk-Tenant-Id": self.tenant_id,
        }

    def update_current_user_language(self, language: str):
        """重置用户语言设置

        :param language: 语言
        """
        try:
            # 包括所有祖先部门
            self.client.update_current_user_language(json={"language": language})
        except JSONResponseError:
            return
        except (APIGatewayResponseError, ResponseError) as e:
            logger.exception(f"call bk user api update_current_user_language error, detail: {e}")
            raise BkLoginGatewayServiceError("call bk user api update_current_user_language error")
