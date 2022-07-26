# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
from builtins import object

from ..base import ComponentAPI


class CollectionUsermgr(object):
    """Collections of Usermgr APIS"""

    def __init__(self, client):
        self.client = client

        # id={username}&with_family=true
        # {"message": "success", "code": 0, "result": true, "request_id": "",
        # "data": [{"id": "8", "family": [{"id": "1", "name": "合作伙伴"}, {"id": "8", "name": "CI"}], "name": "CI"}]}
        self.list_profile_departments = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi/v2/usermanage/list_profile_departments/",
            description="get all user departments via user_id",
        )

        # username to get user_info
        self.list_users = ComponentAPI(
            client=self.client,
            method="GET",
            path="/api/c/compapi/v2/usermanage/list_users/",
            description="get user info via user_id",
        )
