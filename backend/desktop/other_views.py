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
import datetime

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import ugettext as _

from bksuite.utils import get_bksuite_info
from common.constants import DATETIME_FORMAT_STRING
from common.license_utils import check_license


def get_license_notice(request):
    """
    获取许可证提示信息
    :param request:None
    :return: {'result': True/False, 'message': ''}
    """
    is_ok, message, valid_start_time, valid_end_time = check_license()
    # 许可证有效且大于1年，则无需提示
    now = timezone.now()
    one_year = datetime.timedelta(days=settings.LICENSE_AHEAD_NOTICE_DAYS)
    if is_ok and valid_end_time - now >= one_year:
        return JsonResponse({"result": True, "message": ""})
    # 许可证有效，但有效期小于1年 则需要提示
    if is_ok:
        tip_msg = _(u"当前企业版的有效期至%s，请提前15个工作日联系软件供应商提供技术支持") % valid_end_time.strftime("%Y-%m-%d")
        return JsonResponse({"result": False, "message": tip_msg})
    return JsonResponse({"result": False, "message": _(u"%s，请联系管理员处理！") % message})


def get_version_info(request):
    """
    获取版本信息
    :param request:None
    :return: {'result': True/False, 'data': {}, 'message'}
    """
    # check_license
    is_ok, message, valid_start_time, valid_end_time = check_license()
    valid_period = "--"
    expired_time = "--"
    if is_ok:
        valid_period = _(u"%(start_time)s 至 %(end_time)s") % {
            "start_time": valid_start_time.strftime(DATETIME_FORMAT_STRING),
            "end_time": valid_end_time.strftime(DATETIME_FORMAT_STRING),
        }
        expired_time = valid_end_time.strftime(DATETIME_FORMAT_STRING)

    version = settings.BK_VERSION
    return JsonResponse(
        {
            "result": True,
            "data": {"version": version, "valid_period": valid_period, "expired_time": expired_time},
            "message": "",
        }
    )
