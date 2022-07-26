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
from django.conf.urls import url

from user_center import views, wx_views

# 统计应用
urlpatterns = [
    # 首页（账号信息）
    url(r"^$", views.account),
    url(r"^account/$", views.account),
    url(r"^account/modify_user_info/$", views.modify_user_info),
    url(r"^account/change_password/$", views.change_password),
    # 查询绑定状态
    url(r"^weixin/get_bind_status/$", wx_views.get_bind_status),
    # 解绑用户微信信息
    url(r"^weixin/unbind_wx_user_info/$", wx_views.unbind_wx_user_info),
    # 微信公众号
    url(r"^weixin/mp/get_qrcode/$", wx_views.get_qrcode_by_mp),
    url(r"^weixin/mp/callback/$", wx_views.weixin_mp_callback),
    # 微信企业号/企业微信
    url(r"^weixin/qy/get_login_url/$", wx_views.get_login_url_by_qy),
    url(r"^weixin/qy/login_callback/$", wx_views.weixin_qy_login_callback),
    # 组件申请审批
    url(r"^esb_apply/approval/$", views.esb_approval),
    url(r"^esb_apply/get_not_done_record/$", views.get_not_done_esb_record),
    url(r"^esb_apply/save_approval_result/$", views.save_esb_approval_result),
    # 组件申请记录
    url(r"^esb_apply/history/$", views.esb_history),
    url(r"^esb_apply/get_done_record/$", views.get_done_esb_record),
]
