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
"""
开发环境配置
"""

DEBUG = True

# use the static root 'static' in production envs
if not DEBUG:
    STATIC_ROOT = "static"

# 数据库配置信息
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # 默认用mysql
        "NAME": "open_paas",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
    "bksuite": {
        "ENGINE": "django.db.backends.mysql",  # 默认用mysql
        "NAME": "bksuite_common",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}

# domain
PAAS_DOMAIN = "paas.open.bking.com"
# inner domain, use consul domain,  for api
PAAS_INNER_DOMAIN = ""
HTTP_SCHEMA = "http"

# cookie 名称
BK_COOKIE_NAME = "bk_token"
# cookie有效期
BK_COOKIE_AGE = 60 * 60 * 24
# cookie访问域
BK_COOKIE_DOMAIN = ""

# 登录域名
LOGIN_DOMAIN = "paas.open.bking.com"

# ESB Token
ESB_TOKEN = "12345"

CERTIFICATE_DIR = "/"
CERTIFICATE_SERVER_DOMAIN = "127.0.0.1"

try:
    from conf.local_settings import *  # noqa
except ImportError:
    pass
