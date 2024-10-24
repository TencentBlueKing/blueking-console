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

from common.constants import enum

# 提测和上线分类
OperateIDEnum = enum(
    TO_TEST=0,
    TO_ONLINE=1,
    TO_OUTLINE=2,
    IN_TEST=3,
    IN_ONLINE=4,
    IN_OUTLINE=5,
    REGISTER_INFO=6,
    CREATE_DB=7,
    INITIAL_CVS=8,
    GRANT_DB_AUTH=9,
    INITIAL_APP_CODE=10,
    DELETE_APP=11,
)

OPERATE_ID_CHOICES = [
    (OperateIDEnum.TO_TEST, _(u"提测")),
    (OperateIDEnum.TO_ONLINE, _(u"上线")),
    (OperateIDEnum.TO_OUTLINE, _(u"下架")),
    (OperateIDEnum.IN_TEST, _(u"正在提测")),
    (OperateIDEnum.IN_ONLINE, _(u"正在上线")),
    (OperateIDEnum.IN_OUTLINE, _(u"正在下架")),
    (OperateIDEnum.REGISTER_INFO, _(u"基本信息注册")),
    (OperateIDEnum.CREATE_DB, _(u"数据库创建")),
    (OperateIDEnum.INITIAL_CVS, _(u"SVN代码初始化")),
    (OperateIDEnum.GRANT_DB_AUTH, _(u"数据库授权")),
    (OperateIDEnum.INITIAL_APP_CODE, _(u"初始化APP代码")),
    (OperateIDEnum.DELETE_APP, _(u"删除APP")),
]


# 用户操作类型
UserOperateTypeEnum = enum(
    APP_CREATE=1,
    APP_DELETE=2,
    RELEASE_TEST=3,
    RELEASE_ONLINE=4,
    RELEASE_OUTLINE=5,
)

USER_OPERATE_TYPE_CHOICES = [
    (UserOperateTypeEnum.APP_CREATE, _(u"APP创建")),
    (UserOperateTypeEnum.APP_DELETE, _(u"删除APP")),
    (UserOperateTypeEnum.RELEASE_TEST, _(u"APP提测")),
    (UserOperateTypeEnum.RELEASE_ONLINE, _(u"APP上线")),
    (UserOperateTypeEnum.RELEASE_OUTLINE, _(u"APP下架")),
]
