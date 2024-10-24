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
from django.urls import re_path

from analysis import views

# 分析统计
urlpatterns = [
    # 保存app的访问信息
    re_path(r"^app_record_by_user/(?P<app_id_or_code>[a-z0-9_-]+)/$", views.app_record_by_user),
    # 保存app点击量
    re_path(r"^app_liveness_save/$", views.app_liveness_save),
    # 保存app在线时长
    re_path(r"^app_online_time_save/$", views.app_online_time_save),
]
