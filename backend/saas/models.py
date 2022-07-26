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

import os
import time
from builtins import object

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _l

from app.models import App
from common.constants import APP_LOGO_IMG_RELATED, SAAS_APP_LOGO_IMG_RELATED
from saas.manager import SaaSAppManager


class SaaSApp(models.Model):

    code = models.CharField(_l(u"应用编码"), max_length=30, unique=True, help_text=_l(u"此处请用英文字母"))
    name = models.CharField(_l(u"应用名称"), max_length=20)

    # 对应的paas app, 一旦绑定, 不会解绑
    app = models.ForeignKey(to=App, blank=True, null=True, on_delete=models.CASCADE)

    # 正在执行上线的版本, 可能上线失败
    current_version = models.ForeignKey(
        to="SaaSAppVersion", on_delete=models.CASCADE, related_name="current_versions", blank=True, null=True
    )

    # 在线上运行的版本
    online_version = models.ForeignKey(
        to="SaaSAppVersion", on_delete=models.CASCADE, related_name="online_versions", blank=True, null=True
    )

    # NOTE: 测试环境, 正在执行发布测试环境的版本 / 当前测试环境版本及
    current_test_version = models.ForeignKey(
        to="SaaSAppVersion", on_delete=models.CASCADE, related_name="current_test_version", blank=True, null=True
    )
    test_version = models.ForeignKey(
        to="SaaSAppVersion", on_delete=models.CASCADE, related_name="test_versions", blank=True, null=True
    )

    # 应用创建时间
    created_time = models.DateTimeField(_l(u"创建时间"), auto_now_add=True, blank=True, null=True)
    # 应用图标
    logo = models.ImageField(upload_to=APP_LOGO_IMG_RELATED, blank=True, null=True)

    objects = SaaSAppManager()

    @property
    def logo_url(self):
        if self.logo:
            return "%s?v=%s" % (self.logo.url, time.time())
        else:
            # 判断 以 app_code 命名的 logo 图片是否存在
            logo_name = "%s/%s.png" % (APP_LOGO_IMG_RELATED, self.code)
            logo_path = os.path.join(settings.MEDIA_ROOT, logo_name)
            if os.path.exists(logo_path):
                return "%s%s" % (settings.MEDIA_URL, logo_name)

            # 判断是否是上传saas解压生成的文件, 存在的话使用之(saas内置应用上传包中带的logo)
            logo_name = "%s/%s.png" % (SAAS_APP_LOGO_IMG_RELATED, self.code)
            logo_path = os.path.join(settings.MEDIA_ROOT, logo_name)
            if os.path.exists(logo_path):
                return "%s%s" % (settings.MEDIA_URL, logo_name)

            return "%simg/app_logo/default.png" % settings.STATIC_URL

    @property
    def name_display(self):
        if self.app:
            return self.app.name_display
        return _(self.name)

    def __unicode__(self):
        return self.code

    def __str__(self):
        return self.code

    class Meta(object):
        ordering = ("-code",)
        db_table = "paas_saas_app"
        verbose_name = _l(u"SaaS 应用")
        verbose_name_plural = _l(u"SaaS 应用")


class SaaSAppVersion(models.Model):
    """
    SaaSVersion

    逻辑上限制了: 一个version, 一个saas_app
    """

    version = models.CharField(_l(u"版本"), max_length=20)
    # 配置json串
    settings = models.TextField(_l(u"包配置"), blank=True, null=True)

    # 所属的saas app, 当saas app被删除, 级联删除
    saas_app = models.ForeignKey(to="SaaSApp", blank=False, null=False, on_delete=models.CASCADE)
    # 对应文件
    upload_file = models.ForeignKey(to="SaaSUploadFile", on_delete=models.CASCADE, blank=False, null=False)

    updated_at = models.DateTimeField(_l(u"更新时间"), auto_now=True, blank=True, null=True)

    def __unicode__(self):
        return "%s %s %s" % (self.id, self.version, self.upload_file)

    def __str__(self):
        return "%s %s %s" % (self.id, self.version, self.upload_file)

    class Meta(object):
        db_table = "paas_saas_app_version"
        verbose_name = _l(u"SaaS 应用版本")
        verbose_name_plural = _l(u"SaaS 应用版本")


class SaaSUploadFile(models.Model):
    """
    SaaS上传安装包
    """

    name = models.CharField(_l(u"文件名"), max_length=100)
    size = models.IntegerField(_l(u"文件大小"), default=0, blank=True, null=True)
    md5 = models.CharField(u"md5", max_length=32, blank=False, null=False)

    # 重命名, 不要覆盖原来的文件, 即使越来越多也没关系.
    # 保证在数据库里面根据版本寻址能找到
    file = models.FileField(_l(u"文件"), upload_to="saas_files")
    # file = models.FileField(u"文件", upload_to="saas_files", storage=OverwriteStorage())

    uploaded_at = models.DateTimeField(_l(u"上传时间"), auto_now_add=True, db_index=True)

    @property
    def url(self):
        return self.file.url

    @property
    def uploaded_at_display(self):
        if not self.uploaded_at:
            return self.uploaded_at
        t = timezone.localtime(self.uploaded_at)
        return t.strftime("%Y-%m-%d %H:%M:%S %z")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ("-uploaded_at",)
        db_table = "paas_saas_upload_file"
        verbose_name = _l(u"SaaS上传安装包")
        verbose_name_plural = _l(u"SaaS上传安装包")


class OverwriteStorage(FileSystemStorage):
    """
    overwrite the file on disk if the name is the same
    """

    def get_available_name(self, name):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/
        """
        # TODO: 文件不覆盖, 文件重命名为 xxx_V版本号
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name
