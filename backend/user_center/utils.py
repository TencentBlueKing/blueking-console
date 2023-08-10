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
import re
from typing import Optional

from django.conf import settings

from common.constants import ROLECODE_DICT, RoleCodeEnum


def get_smart_paas_domain():
    """
    智能获取paas域名，80端口去除
    """
    host_port = settings.PAAS_DOMAIN.split(":")
    port = host_port[1] if len(host_port) >= 2 else ""
    paas_domain = host_port[0] if port in ["80"] else settings.PAAS_DOMAIN
    return paas_domain


def get_role_display(role: Optional[int]) -> str:
    if not role:
        return ROLECODE_DICT[RoleCodeEnum.STAFF]
    return ROLECODE_DICT.get(role) or ROLECODE_DICT[RoleCodeEnum.STAFF]


def desensitize_phone_number(phone_number):
    # 手机号为空则返回占位符
    if not phone_number:
        return '--'

    # 删除空格
    phone_number = phone_number.replace(" ", "")

    # 大陆手机号
    mainland_mobile_pattern = re.compile(r'^(?:\+?86)?(1\d{10})$')
    # 香港手机号
    hk_mobile_pattern = re.compile(r'^(?:\+?852)(\d{8})$')
    # 澳门手机号
    macao_mobile_pattern = re.compile(r'^(?:\+?853)(\d{8})$')
    # 台湾手机号
    tw_mobile_pattern = re.compile(r'^(?:\+?886)(9\d{8})$')
    # 海外手机号
    overseas_mobile_pattern = re.compile(r'^(\+\d{1,3})(\d{4,})$')
    # 大陆固定电话
    mainland_landline_pattern = re.compile(r'^(\d{3,4}-)(\d{7,8})$')

    # 大陆手机：展示（区号）前 3 位和后 4 位，中间用 4 个 * 代替
    if mainland_mobile_pattern.match(phone_number):
        phone_number = re.sub(mainland_mobile_pattern, r'\1', phone_number)
        return phone_number[:3] + "****" + phone_number[7:]
    # 香港、澳门：展示前2后2，中间用 4 个 * 代替
    elif hk_mobile_pattern.match(phone_number) or macao_mobile_pattern.match(phone_number):
        if hk_mobile_pattern.match(phone_number):
            phone_number = re.sub(hk_mobile_pattern, r'\1', phone_number)
        else:
            phone_number = re.sub(macao_mobile_pattern, r'\1', phone_number)
        return phone_number[:2] + "****" + phone_number[-2:]
    # 台湾：展示前 2后3，中间用 4 个 * 代替
    elif tw_mobile_pattern.match(phone_number):
        phone_number = re.sub(tw_mobile_pattern, r'\1', phone_number)
        return phone_number[:2] + "****" + phone_number[-3:]
    # 海外：只展示地区号和中间4位，占位符用4 个 *
    elif overseas_mobile_pattern.match(phone_number):
        area_code, remaining_digits = re.sub(overseas_mobile_pattern, r'\1 \2', phone_number).split()
        return area_code + "****" + remaining_digits[-4:] + "****"
    # 固定电话：只展示区号和后4位，中间用 4 个 * 代替
    elif mainland_landline_pattern.match(phone_number):
        area_code, local_number = re.sub(mainland_landline_pattern, r'\1 \2', phone_number).split()
        return area_code + "****" + local_number[-4:]
    else:
        return phone_number


def desensitize_email(email: Optional[str]) -> str:
    # 邮箱为空，则返回占位符
    if not email:
        return '--'
    # 邮箱格式非法，则原样返回
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return email

    # 显示前2字符，展示@及@后所有字符
    username, domain = email.split('@')
    return username[:2] + "****@" + domain


def desensitize_qq(qq_number: Optional[str]) -> str:
    # QQ 为空，则返回占位符
    if not qq_number:
        return '--'

    # 展示首尾字符，中间4个*代替
    return qq_number[0] + "****" + qq_number[-1]
