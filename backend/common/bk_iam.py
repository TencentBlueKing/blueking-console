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
from builtins import object

from django.conf import settings
from django.utils.translation import ugettext as _
from iam import IAM, Action, Request, Resource, Subject
from iam.apply.models import (
    ActionWithoutResources,
    ActionWithResources,
    Application,
    RelatedResourceType,
    ResourceInstance,
    ResourceNode,
)

from app.models import App
from common.constants import enum
from common.log import logger

if settings.DEBUG:
    import logging
    import sys

    iam_logger = logging.getLogger("iam")
    iam_logger.setLevel(logging.DEBUG)

    debug_hanler = logging.StreamHandler(sys.stdout)
    debug_hanler.setFormatter(logging.Formatter("%(levelname)s [%(asctime)s] [IAM] %(message)s"))
    iam_logger.addHandler(debug_hanler)
    iam_logger.propagate = True


# enum
PrincipalTypeEnum = enum(USER="user")

ActionEnum = enum(
    ACCESS_DEVELOPER_CENTER="access_developer_center",
    DEVELOP_APP="develop_app",
    MANAGE_SMART="manage_smart",
    OPS_SYSTEM="ops_system",
    MANAGE_APIGATEWAY="manage_apigateway",
)

ActionNameDict = {
    ActionEnum.ACCESS_DEVELOPER_CENTER: _(u"访问开发者中心"),
    ActionEnum.DEVELOP_APP: _(u"开发SaaS应用及外链应用"),
    ActionEnum.MANAGE_SMART: _(u"管理S-mart应用"),
    ActionEnum.OPS_SYSTEM: _(u"系统维护"),
    ActionEnum.MANAGE_APIGATEWAY: _(u"API网关维护"),
}

ResourceTypeEnum = enum(
    APP="app",
)

ResourceTypeNameDict = {
    ResourceTypeEnum.APP: _(u"应用"),
}

# 线上环境走内网，开发环境配置host
BK_IAM_HOST = "%s://%s" % ("http", settings.HOST_IAM_NEW)
BK_PAAS_HOST = "%s://%s" % ("http", settings.PAAS_INNER_DOMAIN)
# bk_paas
SYSTEM_ID = settings.PAAS_APP_ID

APP_CODE = SYSTEM_ID
# SECRET_KEY from settings_*.py, production is __ESB_TOKEN__
APP_SECRET = settings.ESB_TOKEN


class Permission(object):
    def __init__(self):
        self._iam = IAM(APP_CODE, APP_SECRET, BK_IAM_HOST, BK_PAAS_HOST)

    def _make_request_without_resources(self, username, action_id):
        request = Request(
            SYSTEM_ID,
            Subject(PrincipalTypeEnum.USER, username),
            Action(action_id),
            None,
            None,
        )
        return request

    def _make_request_with_resources(self, username, action_id, resources):
        request = Request(
            SYSTEM_ID,
            Subject(PrincipalTypeEnum.USER, username),
            Action(action_id),
            resources,
            None,
        )
        return request

    def _make_request_without_subject(self, action_id, resources):
        request = Request(
            SYSTEM_ID,
            None,
            Action(action_id),
            resources,
            None,
        )
        return request

    # TODO: 处理异常 => try except return false

    def allowed_access_developer_center(self, username):
        """
        访问开发者中心权限
        """
        request = self._make_request_without_resources(username, ActionEnum.ACCESS_DEVELOPER_CENTER)
        return self._iam.is_allowed(request)

    def allowed_manage_smart(self, username):
        """
        smart管理权限
        """
        request = self._make_request_without_resources(username, ActionEnum.MANAGE_SMART)
        return self._iam.is_allowed(request)

    def allowed_ops_system(self, username):
        """
        PaaSAgent和第三方服务管理权限
        """
        request = self._make_request_without_resources(username, ActionEnum.OPS_SYSTEM)
        return self._iam.is_allowed(request)

    def allowed_manage_apigateway(self, username):
        """
        网关管理权限
        """
        request = self._make_request_without_resources(username, ActionEnum.MANAGE_APIGATEWAY)
        return self._iam.is_allowed(request)

    def get_token(self):
        ok, message, token = self._iam.get_token(SYSTEM_ID)
        if not ok:
            logger.error("get token from iam fail: %s, will try again", message)

            # try again
            ok, message, token = self._iam.get_token(SYSTEM_ID)
            if not ok:
                logger.error("get token from iam fail: %s, will return empty string", message)
                return ""
            return token

        return token

    def allowed_develop_app(self, username, app_code):
        """
        app开发权限
        """
        # app = App.objects.get(code=app_code)

        r = Resource(SYSTEM_ID, ResourceTypeEnum.APP, app_code, {})
        resources = [r]
        request = self._make_request_with_resources(username, ActionEnum.DEVELOP_APP, resources)
        return self._iam.is_allowed(request)

    def app_list(self, username):
        """
        用户有权限的应用列表

        拉回策略, 自己算!
        """
        request = self._make_request_without_resources(username, ActionEnum.DEVELOP_APP)

        # 两种策略 1) 实例级别 2) 用户级别
        # 只有条件 code in []
        key_mapping = {"app.id": "code"}

        filters = self._iam.make_filter(request, key_mapping=key_mapping)
        if not filters:
            return []

        apps = App.objects.filter(filters).all()
        return [app.code for app in apps]

    def make_no_app_application(self, action_id, with_access_developer_center=True):
        action = ActionWithoutResources(action_id)

        actions = [action]
        # 申请权限附加多申请一个: 访问开发者中心
        if with_access_developer_center and action_id != ActionEnum.ACCESS_DEVELOPER_CENTER:
            actions.append(ActionWithoutResources(ActionEnum.ACCESS_DEVELOPER_CENTER))

        application = Application(SYSTEM_ID, actions)
        return application

    def make_app_application(self, app_code):
        instance = ResourceInstance([ResourceNode("app", app_code, app_code)])
        related_resource_type = RelatedResourceType(SYSTEM_ID, "app", [instance])

        action = ActionWithResources(ActionEnum.DEVELOP_APP, [related_resource_type])

        # 申请权限附加多申请一个: 访问开发者中心
        actions = [action, ActionWithoutResources(ActionEnum.ACCESS_DEVELOPER_CENTER)]

        application = Application(SYSTEM_ID, actions)
        return application

    def generate_apply_url(self, bk_token, application):
        """
        处理无权限 - 跳转申请列表

        暂时实现不了
        """
        ok, message, url = self._iam.get_apply_url(bk_token, application)
        if not ok:
            logger.error("iam generate apply url fail: %s", message)
            return ""
        return url

    def app_developers(self, app_code):
        """
        获取应用的开发者列表(有这个应用开发权限的用户列表)
        """
        # app = App.objects.get(code=app_code)
        # r = Resource(SYSTEM_ID, ResourceTypeEnum.APP, app_code, {})
        # resources = [r]
        # request = self._make_request_without_subject(ActionEnum.DEVELOP_APP, resources)

        # [{'type': 'user', 'id': 'admin', 'name': u'admin'},
        #  {'type': 'department', 'id': '43657', 'name': '运维中心'},
        #  {'type': u'group', 'id': '24', 'name': u'group1'}]
        # return self._iam.query_subjects(request)
        return []


# def subjects_display(subjects):
#     if not subjects:
#         return ""
#     data = []
#     for subject in subjects:
#         data.append(subject["name"])

#     return ";".join(data)
