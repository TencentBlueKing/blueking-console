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

from django.db import migrations, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Migration(migrations.Migration):
    """全新环境只创建 WxmpAccessToken；已有环境继续走 0001-0014 后删除其余表。"""

    replaces = [
        ("bkcore", "0001_initial"),
        ("bkcore", "0002_auto_20160712_2041"),
        ("bkcore", "0003_load_intial_data"),
        ("bkcore", "0004_auto_20170220_2054"),
        ("bkcore", "0005_appaccount"),
        ("bkcore", "0006_esbchannel_comp_conf"),
        ("bkcore", "0007_auto_20170619_1050"),
        ("bkcore", "0008_auto_20170629_1138"),
        ("bkcore", "0009_wxmpaccesstoken"),
        ("bkcore", "0010_auto_20171110_1004"),
        ("bkcore", "0011_auto_20171116_1205"),
        ("bkcore", "0012_auto_20180622_1815"),
        ("bkcore", "0013_auto_20200617_1201"),
        ("bkcore", "0014_delete_unused_esb_tables"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WxmpAccessToken",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("wx_app_id", models.CharField(max_length=128, verbose_name=_("微信APPID"))),
                ("access_token", models.CharField(max_length=1024, verbose_name=_("凭证"))),
                ("expires", models.DateTimeField(verbose_name=_("凭证过期时间"))),
                (
                    "last_updated_time",
                    models.DateTimeField(default=timezone.now, verbose_name=_("最后访问时间")),
                ),
            ],
            options={
                "db_table": "esb_wxmp_access_token",
                "verbose_name": _("微信公众号AccessToken"),
                "verbose_name_plural": _("微信公众号AccessToken"),
            },
        ),
    ]
