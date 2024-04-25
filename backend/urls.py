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

console URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django.views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # noqa
from django.shortcuts import redirect
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from account.decorators import login_exempt
from healthz import views as healthz_views

urlpatterns = [
    # 首页, 重定向到首页, pattern => /console/  permanent => 301
    url(r"^$", lambda _: redirect("/console/", permanent=True)),
    # 用户账号相关
    url(r"^console/accounts/", include("account.urls")),
    # app应用数据（点击量，访问量，在线时长等）
    url(r"^console/analysis/", include("analysis.urls")),
    # app 统计分析图表（点击量，访问量，在线时长等）
    url(r"^console/app_statistics/", include("app_statistics.urls")),
    # 个人中心
    url(r"^console/user_center/", include("user_center.urls")),
    # 蓝鲸工作台
    url(r"^console/", include("desktop.urls")),
    # 检测桌面是否正常运行
    url(r"^console/healthz/", include("healthz.urls")),
    url(r"^console/ping/", healthz_views.ping),
    # 通知中心
    url(r"^console/notice/", include(("bk_notice_sdk.urls", "notice"), namespace="notice")),
    # 国际化设置相关
    url(r"^console/i18n/", include("bk_i18n.urls")),
    # admin
    path("admin/", admin.site.urls),
]

# 处理JS翻译
urlpatterns += i18n_patterns(
    path('console/jsi18n/i18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
)

# for upload/download
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_serve = login_exempt(django.views.static.serve)
urlpatterns.append(url(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}))
urlpatterns.append(url(r"^console/static/(?P<path>.*)$", static_serve, {"document_root": settings.STATIC_ROOT}))

# for pormetheus metrics
from django_prometheus import exports  # noqa

urlpatterns.append(url(r"^metrics$", login_exempt(exports.ExportToDjangoView), name="prometheus-django-metrics"))
