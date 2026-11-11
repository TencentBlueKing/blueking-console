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

从 KMS 信封加载敏感配置

部署方式沿用 helm-charts 大仓的 KMS 规范：开关 `BK_CONSOLE_KMS_ENABLED` 只读取环境变量，仅接受 "true" 或 "True"；
私钥从环境变量 `BK_CONSOLE_KMS_PRIVATE_KEY` 读取，信封从文件 `/etc/secrets/bk-console-kms` 读取。
私钥或信封不可用、解密失败、必填凭证缺失时阻止启动。
"""

import functools
import json
import logging
import os
from pathlib import Path
from typing import Any, Mapping, Optional

from bk_kms import CryptoBackendUnavailableError, CryptoError, decrypt
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)

KMS_ENABLED_ENV_VAR = "BK_CONSOLE_KMS_ENABLED"
PRIVATE_KEY_ENV_VAR = "BK_CONSOLE_KMS_PRIVATE_KEY"
# 仅供本地开发覆盖信封路径，chart 不设置
ENVELOPE_PATH_ENV_VAR = "BK_CONSOLE_KMS_ENVELOPE_PATH"
DEFAULT_ENVELOPE_PATH = "/etc/secrets/bk-console-kms"


def is_kms_enabled() -> bool:
    # 不能直接 bool()，否则字符串 "false" 也会开启 KMS
    return os.environ.get(KMS_ENABLED_ENV_VAR) in ("true", "True")


def get_kms_setting(key: str, path: str, original: Any, required: bool = False, warn_plaintext: bool = True) -> Any:
    """未开启 KMS 时返回原配置；开启时优先使用信封中的值，未提供时沿用原配置

    :param key: 配置项名，仅用于报错和告警
    :param path: 信封字段路径，如 mysql.open_paas.password
    :param original: 原配置的值
    :param required: 信封与原配置都没有值时是否阻止启动
    :param warn_plaintext: 沿用原配置中的非空值时是否告警
    """
    if not is_kms_enabled():
        return original

    value = _read_credential_field(_decrypt_credentials(), path)
    if value is not None:
        return value
    if required and not original:
        raise ImproperlyConfigured(f"{key} is required, provide it by KMS credential {path}")
    if warn_plaintext and original:
        # 只记录配置名和字段路径，不记录值
        logger.warning("Sensitive setting %s is not provided by KMS (%s), using its plaintext config", key, path)
    return original


@functools.cache
def _decrypt_credentials() -> Mapping[str, Any]:
    """缓存进程内的信封快照，信封更新后需重启进程"""
    private_key = os.environ.get(PRIVATE_KEY_ENV_VAR, "").strip()
    if not private_key:
        raise ImproperlyConfigured(f"KMS requires {PRIVATE_KEY_ENV_VAR}")

    envelope_path = Path(os.environ.get(ENVELOPE_PATH_ENV_VAR) or DEFAULT_ENVELOPE_PATH)
    try:
        envelope = envelope_path.read_text(encoding="utf-8").strip()
        credentials = json.loads(decrypt(envelope=envelope, private_key=private_key))
    except CryptoBackendUnavailableError:
        raise ImproperlyConfigured("KMS SM2/SM4 crypto backend is unavailable") from None
    except (OSError, UnicodeError, ValueError, CryptoError):
        # 不携带原始异常，避免信封或明文内容出现在启动日志中
        raise ImproperlyConfigured("Unable to read or decrypt the KMS credential envelope") from None

    if not isinstance(credentials, dict):
        raise ImproperlyConfigured("The KMS credential envelope must contain a JSON object")
    return credentials


def _read_credential_field(credentials: Mapping[str, Any], path: str) -> Optional[str]:
    """取出信封中的字符串；缺失、null 或空字符串表示未提供，非空节点的类型错误阻止启动"""
    value: Any = credentials
    parts = path.split(".")
    for index, part in enumerate(parts):
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        if not isinstance(value, Mapping):
            raise ImproperlyConfigured(f"KMS requires an object at {'.'.join(parts[:index])}")
        if part not in value:
            return None
        value = value[part]
    if value is None:
        return None
    if not isinstance(value, str):
        raise ImproperlyConfigured(f"KMS requires a string at {path}")
    return value if value.strip() else None
