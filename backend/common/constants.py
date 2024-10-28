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
from django.utils.translation import gettext_lazy as _


def enum(**enums):
    return type("Enum", (), enums)


# app code的正则常量(由小写英文字母、连接符(-)或数字组成 ， SaaS app 支持下划线
CODE_REGEX = "[a-z0-9_-]+"

# 桌面app默认窗口大小
DESKTOP_DEFAULT_APP_WIDTH = 1200
DESKTOP_DEFAULT_APP_HEIGHT = 720

# 权限申请状态（开发者权限和组件权限）
ApprovalResultEnum = enum(APPLYING="applying", PASS="pass", REJECT="reject")

APPROVAL_RESULT_CHOICE = [
    (ApprovalResultEnum.APPLYING, _(u"申请中")),
    (ApprovalResultEnum.PASS, _(u"审批通过")),
    (ApprovalResultEnum.REJECT, _(u"驳回")),
]

# 用户角色
RoleCodeEnum = enum(STAFF=0, SUPERUSER=1, DEVELOPER=2, OPERATOR=3)

ROLECODE_CHOICES = [
    (RoleCodeEnum.STAFF, _(u"普通用户")),
    (RoleCodeEnum.SUPERUSER, _(u"管理员")),
    (RoleCodeEnum.DEVELOPER, _(u"开发者")),
    (RoleCodeEnum.OPERATOR, _(u"职能化用户")),
]

ROLECODE_DICT = dict(ROLECODE_CHOICES)

ROLECODE_LIST = [RoleCodeEnum.STAFF, RoleCodeEnum.SUPERUSER, RoleCodeEnum.DEVELOPER, RoleCodeEnum.OPERATOR]


DATETIME_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"
LICENSE_VAILD_CACHE_KEY = "BK_LICENSE_VALID"

ModeEnum = enum(TEST="test", PROD="prod", ALL="all")

# logo
# 应用logo目录
APP_LOGO_IMG_RELATED = "applogo"
# saas内置应用logo解压目录
SAAS_APP_LOGO_IMG_RELATED = "saaslogo"
