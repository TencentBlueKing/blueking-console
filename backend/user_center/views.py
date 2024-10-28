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
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from account.accounts import Account
from account.decorators import is_superuser_perm
from app.models import App
from app_esb_auth.models import EsbAuthApplyReocrd
from bk_i18n.constants import TIME_ZONE_LIST
from blueking.component.shortcuts import get_client_by_request
from common.constants import ApprovalResultEnum
from common.log import logger
from components import usermgr
from user_center import utils
from user_center.validators import validate_password
from user_center.wx_utlis import get_user_wx_info


def account(request):
    """
    账号信息页面
    """
    username = request.user.username
    if settings.BK_USER_URL:
        reset_password_url = "%s/change_password/" % (settings.BK_USER_URL)
        user_manage_url = settings.BK_USER_URL
    else:
        # 用户管理是新标签页打开，无法通过宣传链接定位到修改密码的页面
        reset_password_url = "%s://%s/o/bk_user_manage/change_password" % (settings.HTTP_SCHEMA, request.get_host())
        # 用户管理首页，用桌面的宣传链接打开
        user_manage_url = "%s://%s/console/?app=%s" % (
            settings.HTTP_SCHEMA,
            request.get_host(),
            settings.BK_USER_APP_CODE,
        )

    # 微信相关
    wx_type, wx_userid = get_user_wx_info(request)

    # 获取用户基本信息
    bk_token = request.COOKIES.get(settings.BK_COOKIE_NAME, None)
    _, data = Account().get_bk_user_info(bk_token)
    role = data.get("bk_role")

    context = {
        "username": username,
        "chname": data.get('chname', '--'),
        "qq": utils.desensitize_qq(data.get('qq')),
        "phone": utils.desensitize_phone_number(data.get('phone')),
        "email": utils.desensitize_email(data.get('email')),
        "role": role,
        "role_display": utils.get_role_display(role),
        "user_manage_url": user_manage_url,
        "reset_password_url": reset_password_url,
        "wx_type": wx_type,
        "wx_userid": wx_userid,
        "timezones": TIME_ZONE_LIST,
    }
    return render(request, "user_center/account.html", context)


def modify_user_info(request):
    """
    修改个人信息
    """
    username = request.user.username

    chname = request.POST.get("chname", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    qq = request.POST.get("qq", "").strip()

    param = {
        "chname": chname,
        "phone": phone,
        "email": email,
        "qq": qq,
    }
    ok, msg = usermgr.update_user_info(username, **param)
    if ok:
        try:
            # do update in console user
            user_model = get_user_model()
            user = user_model._default_manager.get_by_natural_key(username)
            user.chname = chname
            user.save()
        except Exception:
            logger.exception("save user info to db fail after update success from usermgr")

    return JsonResponse({"result": ok, "message": msg})


def change_password(request):
    """
    用户修改密码
    """
    new_password1 = request.POST.get("new_password1", "").strip()
    new_password2 = request.POST.get("new_password2", "").strip()

    # 校验密码
    is_vaild, msg = validate_password(new_password1, new_password2)
    if not is_vaild:
        return JsonResponse({"result": False, "message": msg})

    username = request.user.username
    result, msg = usermgr.reset_password(username, new_password1)
    return JsonResponse({"result": result, "message": msg})


@is_superuser_perm
def esb_approval(request):
    """
    组件申请-待审批页面
    """
    return render(request, "user_center/esb_approval.html", {})


@is_superuser_perm
def get_not_done_esb_record(request):
    """
    获取组件待审批的记录
    """
    draw = int(request.GET.get("draw"))
    # 每页记录数
    page_size = int(request.GET.get("length"))
    # 分片起始位置
    start = int(request.GET.get("start"))
    # 分片结束位置
    end = start + page_size
    records = EsbAuthApplyReocrd.objects.filter(approval_result=ApprovalResultEnum.APPLYING)
    total = records.count()
    part_record = records[start:end]
    # 查询应用名称
    app_code_list = [i.app_code for i in records]
    if translation.get_language() == "en":
        app_code_name_dict = dict(App.objects.filter(code__in=app_code_list).values_list("code", "name"))
    else:
        app_code_name_dict = dict(App.objects.filter(code__in=app_code_list).values_list("code", "name_en"))

    # 组装数据
    data = [
        {
            "operator": i.operator,
            "apply_time": i.create_time_display,
            "app_name": app_code_name_dict.get(i.app_code) or i.app_code,
            "sys_name": i.sys_name,
            "api_name": i.api_name,
            "record_id": i.id,
        }
        for i in part_record
    ]
    return JsonResponse({"data": data, "recordsTotal": total, "recordsFiltered": total, "draw": draw, "error": ""})


@is_superuser_perm
def save_esb_approval_result(request):
    """
    审批结果保存
    """
    try:
        record_id = int(request.POST.get("record_id"))
        record = EsbAuthApplyReocrd.objects.get(id=record_id)
    except Exception:
        return JsonResponse({"result": False, "message": _(u"该申请记录不存在")})

    if record.approval_result != ApprovalResultEnum.APPLYING:
        return JsonResponse({"result": False, "message": _(u"该申请已经审批过了")})

    approval_result = request.POST.get("approval_result")
    if approval_result not in [ApprovalResultEnum.PASS, ApprovalResultEnum.REJECT]:
        return JsonResponse({"result": False, "message": _(u"[%s]非正常审批结果") % approval_result})

    if approval_result == ApprovalResultEnum.PASS:
        # 调用组件进行权限添加
        param = {"component_ids": record.api_id, "added_app_code": record.app_code}
        client = get_client_by_request(request)
        esb_result = client.esb.add_app_component_perm(param)
        if not esb_result.get("result", False):
            msg = (
                "An error occurred while calling a component to add"
                " component permissions to the app, Error message: %s"
            ) % esb_result.get("message", "")
            logger.error(msg)
            return JsonResponse({"result": False, "message": esb_result.get("message", _(u"调用组件审批接口出错"))})

    # 修改记录
    record.approval_result = approval_result
    record.approver = request.user.username
    record.approval_time = timezone.now()
    record.save()

    return JsonResponse({"result": True, "message": ""})


@is_superuser_perm
def esb_history(request):
    """
    组件申请-历史审批记录
    """
    return render(request, "user_center/esb_history.html", {})


@is_superuser_perm
def get_done_esb_record(request):
    """
    获取已审批的esb申请记录
    """
    draw = int(request.GET.get("draw"))
    # 每页记录数
    page_size = int(request.GET.get("length"))
    # 分片起始位置
    start = int(request.GET.get("start"))
    # 分片结束位置
    end = start + page_size
    search_value = request.GET.get("search[value]", "")
    records = EsbAuthApplyReocrd.objects.exclude(approval_result=ApprovalResultEnum.APPLYING)
    total = records.count()
    if search_value:
        records = records.filter(
            Q(operator__icontains=search_value)
            | Q(app_code__icontains=search_value)
            | Q(sys_name__icontains=search_value)
            | Q(api_name__icontains=search_value)
        )
    filter_total = records.count()
    part_record = records[start:end]
    # 查询应用名称
    app_code_list = [i.app_code for i in records]
    if translation.get_language() == "en":
        app_code_name_dict = dict(App.objects.filter(code__in=app_code_list).values_list("code", "name"))
    else:
        app_code_name_dict = dict(App.objects.filter(code__in=app_code_list).values_list("code", "name_en"))
    # 组装数据
    data = [
        {
            "operator": i.operator,
            "apply_time": i.create_time_display,
            "app_name": app_code_name_dict.get(i.app_code) or i.app_code,
            "sys_name": i.sys_name,
            "api_name": i.api_name,
            "approval_result": i.approval_result,
        }
        for i in part_record
    ]
    result = {"data": data, "recordsTotal": total, "recordsFiltered": filter_total, "draw": draw, "error": ""}
    return JsonResponse(result)
