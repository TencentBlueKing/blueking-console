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

企业证书校验等相关通用函数
"""
import os
from builtins import str

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from common.constants import DATETIME_FORMAT_STRING, LICENSE_VAILD_CACHE_KEY
from common.http import http_post
from common.log import logger
from common.utils.time import parse_local_datetime


def _validate_cert_key_file(cert_file, key_file):
    """
    校验本地cert和key文件
    """
    # 检查cert/key文件是否存在
    if not os.path.isfile(cert_file):
        logger.error("The local certificate is unavailable: certificate file (platform.cert) does not exist")
        return False, _(u"证书文件(platform.cert)不存在: %s") % cert_file, None
    if not os.path.isfile(key_file):
        logger.error("The local certificate is unavailable: key file (platform.key) does not exist")
        return False, _(u"密钥文件(platform.key)不存在: %s") % key_file, None
    # 读取证书文件内容
    cert_raw_string = None
    with open(cert_file) as f:
        cert_raw_string = f.read()
    if not cert_raw_string:
        msg = "The local certificate is unavailable: certificate file (platform.cert) is empty or has been damaged"
        logger.error(msg)
        return False, _(u"证书文件(platform.cert)为空或已被损坏"), None
    return True, "", cert_raw_string


def _validate_remote_license(cert_server_url, cert_file, key_file, cert_raw_string):
    """
    请求证书服务器校验证书
    """
    param = {
        "certificate": cert_raw_string,
        "platform": "open_paas",
        "requesttime": timezone.now().strftime(DATETIME_FORMAT_STRING),
    }

    ok, data = http_post(cert_server_url, param, verify=False, cert=(cert_file, key_file))
    if not ok:
        return False, "request license_server error", _(u"license_server请求校验证书异常"), None, None

    if data["result"]:
        return False, data["message"], data["message_cn"], None, None
    return True, "", "", data["validstarttime"], data["validendtime"]


def check_license():
    """
    检查企业正式是否有效
    :return: True/False, message,
    """
    # 未启用证书，则显示有效期为 50 年
    if not settings.IS_CERTIFICATE_SVC_ENABLED:
        valid_start_time = timezone.now()
        valid_end_time = timezone.now() + timezone.timedelta(days=365 * 50)
        return True, "证书校验未启用", valid_start_time, valid_end_time

    client_cert_file_path = str(settings.CLIENT_CERT_FILE_PATH)
    client_key_file_path = str(settings.CLIENT_KEY_FILE_PATH)
    certificate_server_url = str(settings.CERTIFICATE_SERVER_URL)

    # 本地证书文件检查
    is_valid, message, cert_raw_string = _validate_cert_key_file(client_cert_file_path, client_key_file_path)
    if not is_valid:
        return False, message, None, None

    # 远程检查证书
    # 先从缓存中获取
    remote_license_result = cache.get(LICENSE_VAILD_CACHE_KEY)
    if not remote_license_result:
        remote_license_result = _validate_remote_license(
            certificate_server_url, client_cert_file_path, client_key_file_path, cert_raw_string
        )
        # 设置缓存
        cache.set(LICENSE_VAILD_CACHE_KEY, remote_license_result)

    is_valid, message, message_cn, valid_start_time, valid_end_time = remote_license_result

    if not is_valid:
        logger.error(message)
        # TODO to write a function for selecting data of current lageuage
        error_message = message_cn if translation.get_language() in ["zh-hans"] else message
        return False, error_message, None, None

    try:
        # 时间转换
        valid_start_time = parse_local_datetime(valid_start_time, zone=timezone.utc)
        valid_end_time = parse_local_datetime(valid_end_time, zone=timezone.utc)
    except Exception as error:
        logger.exception("An error occurred while checking enterprise certificate conversion time：%s" % error)
        return False, _(u"证书不可用，请求未返回有效期或返回格式有误"), None, None
    return True, _(u"证书校验成功"), valid_start_time, valid_end_time
