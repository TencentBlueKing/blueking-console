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
from builtins import object

from django.conf import settings
from django.db import models

from analysis.manager import AppLivenessManager, AppOnlineTimeRecordManager, AppUseRecordManager
from app.models import App


class AppUseRecord(models.Model):
    """
    用户使用app的记录
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=u"用户")
    app = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name=u"应用")
    use_time = models.DateTimeField(u"添加时间", auto_now_add=True, blank=True, null=True, help_text=u"使用时间")
    access_host = models.CharField(u"访问域名", max_length=128, blank=True, null=True)
    source_ip = models.CharField(u"来源IP", max_length=64, blank=True, null=True)

    objects = AppUseRecordManager()

    def __unicode__(self):
        return "%s(%s)" % (self.user, self.app)

    class Meta(object):
        db_table = "console_analysis_appuserecord"
        verbose_name = u"App访问记录数据"
        verbose_name_plural = u"App访问记录数据"


class AppLiveness(models.Model):
    """
    app页面点击量、活跃度统计
    """

    app = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name=u"应用")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=u"用户", blank=True, null=True
    )
    hits = models.IntegerField(u"点击量", default=0, help_text=u"应用页面点击量")
    add_date = models.DateTimeField(u"添加日期", auto_now_add=True, blank=True, null=True, help_text=u"记录日期")
    access_host = models.CharField(u"访问域名", max_length=128, blank=True, null=True)
    source_ip = models.CharField(u"来源IP", max_length=64, blank=True, null=True)

    objects = AppLivenessManager()

    def __unicode__(self):
        return "%s(%s)" % (self.user, self.app)

    class Meta(object):
        db_table = "console_analysis_appliveness"
        verbose_name = u"app页面点击量活跃度统计"
        verbose_name_plural = u"app页面点击量活跃度统计"


class AppOnlineTimeRecord(models.Model):
    """
    应用在线时长统计
    """

    ONLINE_TIME_TYPE = [(0, "workbench"), (1, "app")]
    app_code = models.CharField(u"应用编码", max_length=32, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=u"用户", blank=True, null=True
    )
    record_type = models.IntegerField(u"统计类型", choices=ONLINE_TIME_TYPE, default=0)
    online_time = models.FloatField(u"在线时长（秒）", default=0.0, help_text=u"在线时长，以秒为单位")
    add_date = models.DateTimeField(u"添加日期", auto_now_add=True, blank=True, null=True, help_text=u"记录日期")
    access_host = models.CharField(u"访问域名", max_length=128, blank=True, null=True)
    source_ip = models.CharField(u"来源IP", max_length=64, blank=True, null=True)

    objects = AppOnlineTimeRecordManager()

    def __unicode__(self):
        return "%s(%s)" % (self.user, self.app_code)

    class Meta(object):
        db_table = "console_analysis_apponlinetimerecord"
        verbose_name = u"app在线时长统计"
        verbose_name_plural = u"app在线时长统计"
