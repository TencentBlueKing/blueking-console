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

from bkapi_client_core.exceptions import APIGatewayResponseError, ResponseError
from django.conf import settings

from apigw.bk_api import Client
from apigw.exceptions import BkLoginGatewayServiceError, BkLoginNoAccessPermisson

logger = logging.getLogger(__name__)


class BkLoginClient:
    def __init__(self):
        client = Client(endpoint=settings.BK_API_URL_TMPL, stage="prod")
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
                raise BkLoginNoAccessPermisson(e.response.json()["error"]["message"])
            raise BkLoginGatewayServiceError("call bk login api error")

        return resp["data"]
