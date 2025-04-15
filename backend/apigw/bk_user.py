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
from bkapi_client_core.apigateway import APIGatewayClient, Operation, OperationGroup, bind_property


class Group(OperationGroup):
    # 批量查询用户展示信息
    batch_query_user_display_info = bind_property(
        Operation,
        name="batch_query_user_display_info",
        method="GET",
        path="/api/v3/open/tenant/users/-/display_info/",
    )
    # 查询用户所在部门列表
    list_user_department = bind_property(
        Operation,
        name="list_user_department",
        method="GET",
        path="/api/v3/open/tenant/users/{bk_username}/departments/",
    )


class Client(APIGatewayClient):
    """Bkapi bk-user client"""

    _api_name = "bk-user"

    api = bind_property(Group, name="api")
