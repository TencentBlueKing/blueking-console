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
# 蓝鲸产品信息表名
PRODUCTION_INFO_TABLE_NAME = "production_info"

# 查询蓝鲸版本的SQL语句
BKSUITE_QUERY_SQL = "SELECT * FROM {table_name} WHERE code='{bksuite_code}'".format(
    table_name=PRODUCTION_INFO_TABLE_NAME, bksuite_code="bksuite"
)

# 查询所有产品信息
ALL_PRODUCTION_QUERY_SQL = "SELECT * FROM {table_name} ORDER BY index".format(table_name=PRODUCTION_INFO_TABLE_NAME)
