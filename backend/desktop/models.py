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
from django.db import models

from app.models import App
from desktop.constants import MARKET_NAV_CHOICES, MarketNavEnum
from desktop.manager import UserAppManager, UserSettingsManager, WallpaperManager


class Wallpaper(models.Model):
    """
    桌面壁纸
    """

    name = models.CharField(u"壁纸名称", max_length=40, blank=True, null=True)
    number = models.IntegerField(u"壁纸编号", default=0, help_text=u"非0值，则必须保证唯一")
    width = models.IntegerField(u"壁纸宽度", blank=True, null=True)
    height = models.IntegerField(u"壁纸高度", blank=True, null=True)
    is_default = models.BooleanField(u"是否为默认壁纸", default=False)

    objects = WallpaperManager()

    def __unicode__(self):
        return self.name

    class Meta(object):
        db_table = "console_desktop_wallpaper"
        verbose_name = u"壁纸管理"
        verbose_name_plural = u"壁纸管理"


class UserSettings(models.Model):
    """
    用户桌面设置
    """

    APPXY_CHOICES = [("x", u"横排列"), ("y", u"竖排列")]
    DOCKPOS_CHOICES = [("top", u"上边"), ("left", u"左边"), ("right", u"右边")]
    SKIN_CHOICES = [("chrome", "Chrome皮肤"), ("default", u"默认"), ("ext", u"Ext皮肤"), ("mac", u"Mac皮肤"), ("qq", u"QQ皮肤")]
    WALLPAPER_TYPE_CHOICES = [
        ("tianchong", u"填充"),
        ("shiying", u"适应"),
        ("pingpu", u"平铺"),
        ("lashen", u"拉伸"),
        ("juzhong", u"居中"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=u"用户")
    appxy = models.CharField(u"APP图标排列方式", choices=APPXY_CHOICES, max_length=10, default="y")
    dockpos = models.CharField(u"应用码头位置", choices=DOCKPOS_CHOICES, max_length=20, default="left")
    skin = models.CharField(u"窗口皮肤", choices=SKIN_CHOICES, max_length=20, default="mac")
    wallpaper_id = models.IntegerField(u"壁纸ID", default=1)
    wallpaper_type = models.CharField(u"壁纸显示方式", choices=WALLPAPER_TYPE_CHOICES, max_length=20, default="tianchong")
    dock = models.TextField(u"[应用码头]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用
    desk1 = models.TextField(u"[桌面1]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用
    desk2 = models.TextField(u"[桌面2]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用
    desk3 = models.TextField(u"[桌面3]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用
    desk4 = models.TextField(u"[桌面4]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用
    desk5 = models.TextField(u"[桌面5]应用id", default="", blank=True, null=True, help_text=u"用“,”相连")  # 应用拖动的时候需要用

    market_nav = models.IntegerField(u"应用市场左侧导航类别", choices=MARKET_NAV_CHOICES, default=MarketNavEnum.APPTAG)

    objects = UserSettingsManager()

    def __unicode__(self):
        return self.user.username

    class Meta(object):
        db_table = "console_desktop_usersettings"
        verbose_name = u"用户桌面设置"
        verbose_name_plural = u"用户桌面设置"


class UserApp(models.Model):
    """
    用户桌面应用、文件夹
    """

    DESK_APP_TYPE_CHOICES = [(0, u"应用"), (1, u"文件夹")]
    APP_POSITION_CHOICES = [
        ("dock", u"应用码头"),
        ("desk1", u"桌面1"),
        ("desk2", u"桌面2"),
        ("desk3", u"桌面3"),
        ("desk4", u"桌面4"),
        ("desk5", u"桌面5"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=u"用户")
    app = models.ForeignKey(App, on_delete=models.CASCADE, verbose_name=u"应用", null=True, help_text=u"文件夹则此字段为空")
    add_time = models.DateTimeField(u"添加时间", auto_now_add=True, blank=True, null=True, help_text=u"添加时间")
    # 文件夹功能 字段
    desk_app_type = models.IntegerField(u"桌面应用类型", choices=DESK_APP_TYPE_CHOICES, default=0)
    folder_name = models.CharField(
        u"文件夹名", max_length=127, null=True, blank=True, help_text=u"如果desk_app_type为0,则该字段不用填写;反之,则必填"
    )
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name=u"APP所在的文件夹")
    # 应用相关
    app_position = models.CharField(u"用户APP所在位置", choices=APP_POSITION_CHOICES, max_length=20, default="desk1")

    objects = UserAppManager()

    def __unicode__(self):
        return "%s-%s" % (self.user, self.app)

    class Meta(object):
        db_table = "console_desktop_userapp"
        unique_together = ("user", "app")
        ordering = ["id"]
        verbose_name = u"用户桌面应用"
        verbose_name_plural = u"用户桌面应用"
