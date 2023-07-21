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

环境配置 - 环境变量读取
"""

import environ
import urllib3

env = environ.Env()

# Generic Django project settings
DEBUG = env.bool("DEBUG", False)

# 数据库配置信息
DATABASES = {
    "default": {
        "ENGINE": env.str("BK_PAAS_DATABASE_ENGINE", "django.db.backends.mysql"),
        "NAME": env.str("BK_PAAS_DATABASE_NAME", "open_paas"),
        "USER": env.str("BK_PAAS_DATABASE_USER"),
        "PASSWORD": env.str("BK_PAAS_DATABASE_PASSWORD"),
        "HOST": env.str("BK_PAAS_DATABASE_HOST", ""),
        "PORT": env.int("BK_PAAS_DATABASE_PORT"),
    }
}

# 是否展示蓝鲸产品版本信息
IS_BK_SUITE_ENABLED = env.bool("IS_BK_SUITE_ENABLED", False)
if IS_BK_SUITE_ENABLED:
    DATABASES['bksuite'] = {
        "ENGINE": env.str("BK_PAAS_DATABASE_ENGINE", "django.db.backends.mysql"),
        "NAME": env.str("BK_SUITE_DATABASE_NAME", "bksuite_common"),
        "USER": env.str("BK_SUITE_DATABASE_USER", ""),
        "PASSWORD": env.str("BK_SUITE_DATABASE_PASSWORD", ""),
        "HOST": env.str("BK_SUITE_DATABASE_HOST", ""),
        "PORT": env.int("BK_SUITE_DATABASE_PORT", ""),
    }

# 与 ESB 通信的密钥
ESB_TOKEN = env.str("BK_PAAS_SECRET_KEY")

# website
# domain
PAAS_DOMAIN = env.str("BK_PAAS_PUBLIC_ADDR")
# schema = http/https, default http,
HTTP_SCHEMA = env.str("BK_PAAS_HTTP_SCHEMA", "http")

# cookie访问域
BK_COOKIE_DOMAIN = "." + env.str("BK_DOMAIN")

# 内部访问地址，在配置的时候就添加上协议，防止与上面的 HTTP_SCHEMA 概念冲突
# 统一登录服务API访问地址
LOGIN_HOST = env.str("BK_LOGIN_API_URL", "http://bk-login-web")
BK_COMPONENT_API_URL = env.str("BK_COMPONENT_API_URL", "http://bkapi.example.com")
BK_IAM_API_URL = env.str("BK_IAM_API_URL", "http://bkiam-web")

# 登录访问的域名，代码中会自动拼接 /login/ 地址
# LOGIN_DOMAIN = env.str("BK_LOGIN_DOMAIN", "paas.example.com")
# PaaS3.0 开发者中心的访问地址，不填则展示 PaaS2.0 开发者中心访问地址
BK_PAAS3_URL = env.str("BK_PAAS3_URL", "")

# 兼容二进制版本的变量
PAAS_INNER_DOMAIN = urllib3.util.parse_url(BK_COMPONENT_API_URL).host
HOST_IAM_NEW = urllib3.util.parse_url(BK_IAM_API_URL).host
BK_USER_APP_CODE = "bk_usermgr"
# 用户管理访问地址
BK_USER_URL = env.str("BK_USER_URL", "")

# 证书服务
IS_CERTIFICATE_SVC_ENABLED = env.bool("BK_PAAS_CONSOLE_IS_CERTIFICATE_SVC_ENABLED", False)
CERTIFICATE_DIR = env.str("BK_PAAS_CONSOLE_CERT_PATH", "")
CERTIFICATE_SERVER_DOMAIN = env.str("BK_PAAS_CONSOLE_CERT_SERVER_LOCAL_ADDR", "")

# 是否接入权限中心
IS_IAM_ENABLED = env.bool("IS_IAM_ENABLED", False)

# host for cc
HOST_CC = env.str("BK_CMDB_ADDR", "")
# host for job
HOST_JOB = env.str("BK_JOB_ADDR", "")

# 蓝鲸版本号
BK_VERSION = env.str("BK_VERSION", "7.0")


try:
    from conf.local_settings import *  # noqa
except ImportError:
    pass
