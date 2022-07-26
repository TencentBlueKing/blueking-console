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
from functools import wraps

from django.http import JsonResponse
from django.utils.translation import ugettext as _

from user_center.wx_utlis import get_user_wx_info


def is_unbound_weixin(view_func):
    """
    检查是否未绑定
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        wx_type, wx_userid = get_user_wx_info(request)
        if not wx_type:
            return JsonResponse({"result": False, "message": _(u"系统管理员未启用微信通知组件")})
        if wx_userid:
            return JsonResponse({"result": False, "message": _(u"您已绑定微信，无需再绑定")})
        return view_func(request, *args, **kwargs)

    return _wrapped_view
