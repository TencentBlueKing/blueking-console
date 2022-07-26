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
        ('saas', '0006_auto_20161111_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='saasapp',
            name='current_test_version',
            field=models.ForeignKey(related_name='current_test_version', on_delete=models.CASCADE, blank=True, to='saas.SaaSAppVersion', null=True),
        ),
        migrations.AddField(
            model_name='saasapp',
            name='test_version',
            field=models.ForeignKey(related_name='test_versions', on_delete=models.CASCADE, blank=True, to='saas.SaaSAppVersion', null=True),
        ),
        migrations.AddField(
            model_name='saasappversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4', null=True),
        ),
    ]
