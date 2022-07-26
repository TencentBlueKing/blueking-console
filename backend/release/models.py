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

from django.db import models
from django.utils import timezone

from app.constants import STATE_CHOICES
from app.models import App
from common.log import logger
from release.constants import OPERATE_ID_CHOICES, USER_OPERATE_TYPE_CHOICES


class ReleaseRecordManager(models.Manager):
    def create_record(self, app_code, app_old_state, operate_user, operate_id, is_success):
        """
        创建记录
        """
        record_obj = Record.objects.create(
            app_code=app_code,
            app_old_state=app_old_state,
            operate_user=operate_user,
            operate_id=operate_id,
            is_success=is_success,
            operate_time=timezone.now(),
        )
        return record_obj


class Record(models.Model):
    """
    记录应用提测、上线、下架操作信息
    """

    app_code = models.CharField(u"对应的appcode", max_length=30, db_index=True)
    operate_id = models.IntegerField(u"操作标识", choices=OPERATE_ID_CHOICES, help_text=u"0为提测操作，1为上线操作", db_index=True)
    operate_user = models.CharField(u"操作人", max_length=50, blank=True, null=True, help_text=u"进行上线或提测操作的人")

    app_old_state = models.SmallIntegerField(u"操作前app的状态", choices=STATE_CHOICES, help_text=u"操作前app的状态", default=1)
    # = 记录第一次生成的时间
    operate_time = models.DateTimeField(u"操作时间", auto_now_add=True, blank=True, null=True, db_index=True)
    is_success = models.BooleanField(u"操作是否成功", default=False, help_text=u"提测或上线操作是否成功", db_index=True)
    is_tips = models.BooleanField(u"显示新标志", default=False, help_text=u"是否在logo上添加更新提示")
    is_version = models.BooleanField(u"显示新特性", default=False, help_text=u"是否在新应用应用打开时显示该版本更新特性")
    version = models.CharField(u"版本号", max_length=50, blank=True, null=True, help_text=u"需要显示的版本号信息")
    message = models.TextField(u"操作返回信息", blank=True, null=True, help_text=u"执行提测或上线操作后脚本的返回信息")
    event_id = models.CharField(u"Event_id", max_length=36, blank=True, null=True, db_index=True)
    # 后台任务执行额外输出
    extra_data = models.TextField(u"额外执行结果数据", blank=True, null=True, help_text=u"json串存储")

    objects = ReleaseRecordManager()

    @property
    def operate_time_display(self):
        if not self.operate_time:
            return ""
        return timezone.localtime(self.operate_time).strftime("%Y-%m-%d %X")

    def __unicode__(self):
        return "%s" % (self.app_code)

    class Meta(object):
        db_table = "paas_release_record"
        verbose_name = u"应用部署操作信息"
        verbose_name_plural = u"应用部署操作信息"
        app_label = "release"


class Version(models.Model):
    """
    存储app版本信息
    """

    app = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name=u"应用")
    version = models.CharField(u"app版本号", max_length=30, help_text=u"格式：x.x.x，只允许包含数字")
    code_addr = models.CharField(u"拉取的代码地址", max_length=200, blank=True, null=True)
    publisher = models.CharField(u"版本发布者", max_length=30)
    pubdate = models.DateTimeField(u"发布时间", auto_now_add=True, blank=True, null=True, db_index=True)
    desc = models.TextField(u"版本描述", blank=True, null=True)

    @property
    def pubdate_display(self):
        if not self.pubdate:
            return ""
        return timezone.localtime(self.pubdate).strftime("%Y-%m-%d %H:%M:%S")

    def __unicode__(self):
        return "%s(%s)" % (self.app.name, self.version)

    class Meta(object):
        db_table = "paas_release_version"
        verbose_name = u"应用发布版本信息"
        verbose_name_plural = u"应用发布版本信息"
        app_label = "release"


class VersionDetail(models.Model):
    """
    存放应用每个版本对应的特征信息和bugs信息
    """

    features = models.TextField(u"更新特性", help_text=u"记录该版本特性信息", blank=True, null=True, default=None)
    bug = models.TextField(u"修复bug", help_text=u"记录修复的bug信息", blank=True, null=True, default=None)
    app_version = models.ForeignKey(Version, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.features

    class Meta(object):
        db_table = "paas_release_versiondetail"
        verbose_name = u"应用特征信息"
        verbose_name_plural = u"应用特征信息"
        app_label = "release"


class UserOperateRecordManager(models.Manager):
    def create_operate_record(self, app_code, username, operate_type, before_data="", arfter_data="", extra_data=""):
        """
        创建操作记录
        @param app_code: app编码
        @param username: 操作人
        @param operate_type: 操作类型
        @param before_data: 操作前数据
        @param arfter_data: 操作后数据
        @param extra_data: 其他数据
        """
        try:
            UserOperateRecord(
                app_code=app_code,
                username=username,
                before_data=before_data,
                arfter_data=arfter_data,
                operate_time=timezone.now(),
                operate_type=operate_type,
                extra_data=extra_data,
            ).save()
            result = True
        except Exception as e:
            logger.exception("record user operation fail，error：%s" % e)
            result = False
        return result


class UserOperateRecord(models.Model):
    """
    用户操作流水日志
    """

    app_code = models.CharField(u"操作的app", max_length=30)
    username = models.CharField(u"操作人", max_length=50)
    before_data = models.TextField(u"操作前数据", blank=True, null=True)
    arfter_data = models.TextField(u"操作后数据", blank=True, null=True)
    operate_time = models.DateTimeField(u"操作时间", auto_now_add=True)
    operate_type = models.IntegerField(u"操作类型", default=0, choices=USER_OPERATE_TYPE_CHOICES)
    extra_data = models.TextField(u"其他说明", blank=True, null=True)

    objects = UserOperateRecordManager()

    def __unicode__(self):
        return "%s" % (self.app_code)

    class Meta(object):
        db_table = "paas_release_useroperaterecord"
        verbose_name = u"用户操作流水日志"
        verbose_name_plural = u"用户操作流水日志"
        app_label = "release"
