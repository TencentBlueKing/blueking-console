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

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20190123_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='open_mode',
            field=models.CharField(default=b'desktop', max_length=20, verbose_name='\u5e94\u7528\u6253\u5f00\u65b9\u5f0f', choices=[(b'desktop', b'\xe6\xa1\x8c\xe9\x9d\xa2'), (b'new_tab', b'\xe6\x96\xb0\xe6\xa0\x87\xe7\xad\xbe')]),
        ),
    ]
