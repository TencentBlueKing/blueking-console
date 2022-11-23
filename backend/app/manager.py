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
from __future__ import division

from django.db import models
from past.utils import old_div


class AppTagManager(models.Manager):
    def get_all_tags_with_100id(self):
        """
        获取所有分类，并将返回的ID*100，以便应用市场分类的筛选,与创建者分类区分开来
        """
        alltags = self.all()
        tags = [(100 * tag.id, tag.name_display) for tag in alltags if tag]
        return tags

    def get_tags_by_100id(self, search_id):
        """
        筛选id=search_id/100的应用分类
        """
        search_id = old_div(search_id, 100)
        if self.filter(id=search_id).exists():
            return self.get(id=search_id)
        return None
