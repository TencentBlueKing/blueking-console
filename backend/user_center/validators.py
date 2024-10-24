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
from django.utils.translation import gettext as _


def validate_password(password1, password2):
    """
    检查2次密码的一致性
    """
    if not all([password1, password2]):
        return False, _(u"密码不能为空")
    if password1 != password2:
        return False, _(u"两次输入的新密码不一致")
    return True, ""
