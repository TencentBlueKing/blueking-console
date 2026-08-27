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

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class WxmpAccessToken(models.Model):
    """保存微信开放平台业务的 AccessToken"""

    wx_app_id = models.CharField(_("微信APPID"), max_length=128)
    access_token = models.CharField(_("凭证"), max_length=1024)
    expires = models.DateTimeField(_("凭证过期时间"))
    last_updated_time = models.DateTimeField(_("最后访问时间"), default=timezone.now)

    class Meta:
        db_table = "esb_wxmp_access_token"
        verbose_name = _("微信公众号AccessToken")
        verbose_name_plural = _("微信公众号AccessToken")

    def __str__(self):
        return self.wx_app_id
