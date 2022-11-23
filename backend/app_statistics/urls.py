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
from django.conf.urls import url

from app_statistics import views

# 统计应用
urlpatterns = [
    # 获取所有用户
    url(r"^get_all_user/$", views.get_all_user),
    # 获取所有应用
    url(r"^get_all_app/$", views.get_all_app),
    # 获取所有开发者
    # url(r'^get_all_app_developer/$', views.get_all_app_developer),
    # 首页，默认在线时长统计
    url(r"^$", views.app_statistics_page, {"template_name": "online_time"}),
    # 页面选择（在线时长，活跃度，访问量，应用负责人，应用更新情况）
    url(r"^(?P<template_name>[a-z_]+)/$", views.app_statistics_page),
    # 在线时长（按照时间）
    url(r"^online_time/by_time/$", views.online_time_by_time),
    # 在线时长（按照用户）
    url(r"^online_time/by_user/$", views.online_time_by_user),
    # 在线时长（按照应用）
    url(r"^online_time/by_app/$", views.online_time_by_app),
    # 访问量（按照时间）
    url(r"^visit/by_time/$", views.visit_by_time),
    # 访问量（按照应用）
    url(r"^visit/by_app/$", views.visit_by_app),
    # 活跃度（按照时间）
    url(r"^liveness/by_time/$", views.liveness_by_time),
    # 活跃度（按照应用）
    url(r"^liveness/by_app/$", views.liveness_by_app),
    # 应用负责人（按照开发负责人）
    # url(r'^developer/by_developer/$', views.developer_by_developer),
    # 应用更新情况
    url(r"^app_update/by_new_online/$", views.app_update_by_new_online),
]
