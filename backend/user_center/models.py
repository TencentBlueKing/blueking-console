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

from django.db import models

from user_center.manager import WxBkUserTmpRecordManager


class WxBkUserTmpRecord(models.Model):
    """
    微信与蓝鲸用户绑定过程临时表（后续可迁移到redis中，并设置过期时间）
    """

    username = models.CharField(u"用户名", max_length=32)
    bk_token = models.CharField(u"登录态token", max_length=255)
    wx_ticket = models.CharField(u"微信临时标识(state或二维码ticket)", max_length=127, unique=True, db_index=True)
    create_time = models.DateTimeField(u"创建时间", auto_now_add=True, blank=True, null=True)

    objects = WxBkUserTmpRecordManager()

    class Meta(object):
        verbose_name = u"微信与蓝鲸用户绑定过程临时表"
        verbose_name_plural = u"微信与蓝鲸用户绑定过程临时表"
        db_table = "console_wx_bkuser_tmp_record"
        app_label = "user_center"

    def __unicode__(self):
        return self.username
