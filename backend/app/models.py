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
import os
from builtins import object, str  # noqa

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.deletion import SET_NULL
from django.utils import timezone
from django.utils.translation import gettext as _
from past.builtins import cmp  # noqa

from app.constants import (
    BLUEKING_CREATER_DICT,
    DB_TYPE_CHOICES,
    LANGUAGE_CHOICES,
    OPENMODE_CHOICES,
    STATE_CHOICES,
    STATE_CHOICES_DISPALY_DICT,
    VCS_TYPE_CHOICES,
)
from app.manager import AppTagManager
from common.constants import DEFAULT_TENANT_ID, AppTenantMode

APP_LOGO_IMG_RELATED = "applogo"


class AppTags(models.Model):
    """
    应用所属分类
    """

    name = models.CharField(u"分类名称", max_length=20, unique=True)
    code = models.CharField(u"分类英文ID", max_length=30, unique=True)
    index = models.IntegerField(u"排序", default=0, help_text=u"降序排序，即 9 在 0 之前")

    objects = AppTagManager()

    @property
    def name_display(self):
        if not self.name:
            return self.name
        return _(self.name)

    def __unicode__(self):
        return "%s(%s)" % (self.code, self.name)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ("index",)
        db_table = "paas_apptags"
        verbose_name = u"应用分类信息"
        verbose_name_plural = u"应用分类信息"


class AppManager(models.Manager):
    """
    应用数据库操作
    """

    def get_queryset(self):
        """
        重写 查询
        """
        return super(AppManager, self).get_queryset().filter(is_sysapp=False, is_display=True)

    def filter_by_tenant_id(self, tenant_id: str):
        """按租户过滤应用"""
        if not settings.ENABLE_MULTI_TENANT_MODE:
            return self.get_queryset()

        # 返回全租户应用 + 本租户的应用
        return self.get_queryset().filter(
            Q(app_tenant_mode=AppTenantMode.GLOBAL) | Q(app_tenant_mode=AppTenantMode.SINGLE, app_tenant_id=tenant_id)
        )


class App(models.Model):
    """
    应用基本信息表
    """

    name = models.CharField(u"应用名称", max_length=20)
    code = models.CharField(u"应用编码", max_length=30, unique=True, help_text=u"此处请用英文字母")
    introduction = models.TextField(u"应用简介")

    name_en = models.CharField(u"英文应用名称", max_length=30, blank=True, null=True)
    introduction_en = models.TextField(u"英文应用简介", blank=True, null=True)

    creater = models.CharField(u"创建者", max_length=20, blank=True, null=True)
    # 等于, 新增记录的时间
    created_date = models.DateTimeField(u"创建时间", auto_now_add=True, blank=True, null=True, db_index=True)

    state = models.SmallIntegerField(u"应用开发状态", choices=STATE_CHOICES, help_text=u"app的开发状态", default=1)
    tags = models.ForeignKey(AppTags, help_text=u"应用分类", blank=True, null=True, on_delete=SET_NULL)
    is_already_test = models.BooleanField(u"是否已经提测", default=False, help_text=u"app在测试环境下架或者开发中状态，修改该字段为False。")
    is_already_online = models.BooleanField(u"是否已经上线", default=False, help_text=u"app正式环境未下架，该字段为True。")

    first_test_time = models.DateTimeField(u"应用首次提测时间", help_text=u"记录应用首次提测时间", blank=True, null=True, db_index=True)
    first_online_time = models.DateTimeField(
        u"应用首次上线时间", help_text=u"记录应用首次上线时间", blank=True, null=True, db_index=True
    )
    # 开发者信息
    developer = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=u"开发者", related_name="developers")
    # APP语言
    language = models.CharField(
        u"语言", choices=LANGUAGE_CHOICES, default="python", max_length=50, blank=True, null=True
    )

    # celery
    is_use_celery = models.BooleanField(u"app是否使用celery", default=False, help_text=u"选项: true(是)，false(否)")
    is_use_celery_beat = models.BooleanField(u"app是否使用定时任务", default=False, help_text=u"选项: true(是)，false(否)")

    # PaaS3.0 的 app_secret 长度为 50, 加密会更长
    auth_token = models.CharField("Token", max_length=255, blank=True, null=True)
    # 部署的激活码,暂时不用，默认值为null
    deploy_token = models.TextField("deploy_token", blank=True, null=True)
    # 是否作为SaaS服务，即通过直接上传包部署
    is_saas = models.BooleanField("是否为SaaS服务", default=False, help_text=u"SaaS服务，即通过直接上传包部署")
    # 应用图标
    logo = models.ImageField(upload_to=APP_LOGO_IMG_RELATED, blank=True, null=True, max_length=500)
    # 桌面应用基本属性
    width = models.IntegerField(u"app页面宽度", blank=True, null=True, help_text=u"应用页面宽度，必须为整数，单位为px")
    height = models.IntegerField(u"app页面高度", blank=True, null=True, help_text=u"应用页面高度，必须为整数，单位为px")
    is_max = models.BooleanField(u"是否默认窗口最大化", default=False)
    is_setbar = models.BooleanField(u"窗口是否详情等按钮", default=True, help_text=u"选项: true(有)，false(无)")
    is_resize = models.BooleanField(u"是否能对窗口进行拉伸", default=True, help_text=u"选项：true(可以拉伸)，false(不可以拉伸)")
    use_count = models.IntegerField(u"使用人数", default=0, help_text=u"添加了该应用的人数，note：用户卸载应用后，要相应的减1")
    is_default = models.BooleanField(u"是否为默认应用", default=False, help_text=u"默认应用将在用户首次进入工作台时自动到用户桌面")
    is_display = models.BooleanField(u"是否在桌面展示", default=True, help_text=u"选项: true(有)，false(无)")
    open_mode = models.CharField(u"应用打开方式", max_length=20, choices=OPENMODE_CHOICES, default="new_tab")

    # 第三方应用
    is_third = models.BooleanField("是否为第三方应用", default=False, help_text=u"第三方应用，即外部应用，不走自动部署")
    external_url = models.CharField(u"第三方应用URL", max_length=255, help_text=u"当且仅当应用类型为第三方应用时必填", blank=True, null=True)
    # 默认内部应用, 为了获取esb鉴权(esb加白)而生成securt_key的给其他系统调用esb使用 而生成的应用
    is_sysapp = models.BooleanField(
        "是否为系统间应用", default=False, help_text=u"为了获取esb鉴权(esb加白)而生成securt_key的给其他系统调用esb使用 而生成的应用"
    )
    # 平台级别应用(cc, ijobs等)
    is_platform = models.BooleanField("是否为平台级应用", default=False, help_text=u"平台应用（配置平台、作业平台等）")
    # 轻应用
    is_lapp = models.BooleanField(u"是否为轻应用", default=False, help_text=u"标准运维创建的应用")

    # NOTE: should be visiable_labels, without _
    visiable_labels = models.CharField(u"可见范围标签", max_length=1024, blank=True, null=True)
    # 应用评分
    star_num = models.DecimalField(u"星级评分", default=0.00, max_digits=5, decimal_places=2, null=True)

    # 在 PaaS3.0 上创建的应用，ESB/APIGW 会从这个表获取应用鉴权信息，所以需要把 PaaS3.0 应用的 app_code/app_secret 同步到这个表中
    from_paasv3 = models.BooleanField(u"是否 Paas3.0 上创建的应用", default=False)
    # 已经迁移到 PaaS3.0 的应用，则 PaaS2.0 的开发中心不再展示这些应用
    migrated_to_paasv3 = models.BooleanField(u"是否已经迁移到 Paas3.0", default=False)

    # app_tenant_mode 和 app_tenant_id 字段共同控制了应用的“可用范围”，可能的组合包括：
    #
    # - app_tenant_mode: "global", app_tenant_id: ""，表示应用在全租户范围内可用。
    # - app_tenant_mode: "single", app_tenant_id: "foo"，表示应用仅在 foo 租户范围内可用。
    #
    # 应用的“可用范围”将影响对应租户的用户是否可在桌面上看到此应用，以及是否能通过应用链接访问
    # 应用（不在“可用范围”内的用户请求将被拦截）。
    #
    # ## app_tenant_id 和 tenant_id 字段的区别
    #
    # 虽然这两个字段都存储“租户”，且值可能相同，但二者有本质区别。tenant_id 是系统级字段，值
    # 总是等于当前这条数据的所属租户，它确定了数据的所有权。而 app_tenant_id 是业务功能层面的
    # 字段，它和 app_tenant_mode 共同控制前面提到的业务功能——应用“可用范围”。
    #
    app_tenant_mode = models.CharField(
        verbose_name="应用租户模式",
        max_length=16,
        default=AppTenantMode.GLOBAL,
        help_text="应用在租户层面的可用范围，可选值：全租户(global)、单租户（single）",
    )
    app_tenant_id = models.CharField(
        verbose_name="应用租户 ID",
        max_length=32,
        default="",
        help_text="应用对哪个租户的用户可用，当应用租户模式为全租户时，本字段值为空",
        blank=True,
    )
    tenant_id = models.CharField(
        verbose_name="租户 ID",
        max_length=32,
        db_index=True,
        default=DEFAULT_TENANT_ID,
        help_text="本条数据的所属租户",
    )

    objects = AppManager()

    def _del_exist_file(self, name):
        _file = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(_file):
            os.remove(_file)

    def tag_name(self):
        if self.tags and self.tags.name_display:
            return self.tags.name_display
        return u"其它"

    @property
    def state_display(self):
        return STATE_CHOICES_DISPALY_DICT.get(self.state)

    @property
    def saas_state_display(self):
        if self.state == 1:
            return u"未部署"
        return STATE_CHOICES_DISPALY_DICT.get(self.state)

    @property
    def created_date_display(self):
        if not self.created_date:
            return self.created_date
        return timezone.localtime(self.created_date).strftime("%Y-%m-%d")

    @property
    def first_test_time_display(self):
        if not self.first_test_time:
            return self.first_test_time
        return timezone.localtime(self.first_test_time).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def first_online_time_display(self):
        if not self.first_online_time:
            return self.first_online_time
        return timezone.localtime(self.first_online_time).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def introduction_display(self):
        if not self.introduction:
            return self.introduction
        return _(self.introduction).replace("\n", "<br/>")

    @property
    def app_test_url(self):
        if self.is_third:
            return self.external_url
        return settings.APP_TEST_URL.format(app_code=self.code)

    @property
    def app_pro_url(self):
        # 第三方应用和 PaaS3.0 的应用都直接从字段中获取
        if self.is_third or self.is_in_paas3:
            return self.external_url
        return settings.APP_PROD_URL.format(app_code=self.code)

    @property
    def creater_display(self):
        if self.creater not in BLUEKING_CREATER_DICT:
            return self.creater
        return _(self.creater)

    @property
    def name_display(self):
        return self.name

    @property
    def name_en_display(self):
        return self.name_en

    @property
    def is_in_paas3(self):
        """是否运行在 PaaS3.0，包括在 PaaS3.0 上创建的应用和已经迁移到 PaaS3.0 的应用"""
        return self.from_paasv3 or self.migrated_to_paasv3

    def __unicode__(self):
        return "%s(%s)" % (self.code, self.name)

    def __str__(self):
        return self.name

    class Meta(object):
        db_table = "paas_app"
        verbose_name = u"应用基本信息"
        verbose_name_plural = u"应用基本信息"
        # 应用名称租户内唯一
        unique_together = ("app_tenant_id", "name")


class SecureInfo(models.Model):
    """
    APP 安全验证相关信息
    """

    app_code = models.CharField(u"对应的appcode", max_length=30, unique=True)

    # 源代码版本信息
    vcs_type = models.SmallIntegerField(u"版本控制类型", choices=VCS_TYPE_CHOICES, help_text=u"app的开发状态", default=1)
    vcs_url = models.CharField(u"版本库URL", max_length=1024, blank=True, null=True)
    vcs_username = models.CharField(u"版本库用户名", max_length=50, blank=True, null=True)
    vcs_password = models.CharField(u"版本库密码", max_length=50, blank=True, null=True)

    # App数据库信息
    db_type = models.CharField(
        u"数据库类型", choices=DB_TYPE_CHOICES, default="mysql", max_length=20, blank=True, null=True
    )
    db_host = models.CharField(u"数据库HOST", max_length=1024, blank=True, null=True)
    db_port = models.IntegerField(u"数据库PORT", default=3306, blank=True, null=True)
    db_name = models.CharField(u"数据库名称", max_length=30, blank=True, null=True)
    db_username = models.CharField(u"数据库用户名", max_length=50, blank=True, null=True)
    db_password = models.CharField(u"数据库密码", max_length=50, blank=True, null=True)

    @property
    def vcs_type_text(self):
        text = dict(VCS_TYPE_CHOICES).get(self.vcs_type)
        if not text:
            return "unknow"
        return text.lower()

    def __unicode__(self):
        return self.app_code

    class Meta(object):
        db_table = "paas_app_secureinfo"
        verbose_name = u"应用安全相关信息"
        verbose_name_plural = u"应用安全相关信息"


class AppStar(models.Model):
    """
    app星级评分
    """

    app = models.ForeignKey(App, null=True, on_delete=SET_NULL, verbose_name=u"应用")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=SET_NULL, verbose_name=u"评分的用户"
    )
    star_num = models.DecimalField(u"星级评分", default=0.00, max_digits=5, decimal_places=2)
    star_time = models.DateTimeField(u"评分时间", auto_now_add=True)

    def __unicode__(self):
        return "%s-%s-%s" % (self.app, self.user, self.star_num)

    class Meta:
        db_table = "paas_app_star"
        verbose_name = u'应用评分信息'
        verbose_name_plural = u'应用评分信息'
