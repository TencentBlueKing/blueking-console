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
import datetime

from django.db import models
from django.db.models import Sum

from app.models import App
from common.log import logger


class AppOnlineTimeRecordManager(models.Manager):
    def get_onlinetime(self, stime, etime, app_code, user_name):
        """
        获取经过过滤的在线时长数据
        """
        all_online_time = self.filter()
        # 筛选
        if stime:
            all_online_time = all_online_time.filter(add_date__gte=stime)
        if etime:
            all_online_time = all_online_time.filter(add_date__lte=etime)
        if app_code:
            all_online_time = all_online_time.filter(app_code=app_code)
        if user_name:
            all_online_time = all_online_time.filter(user__username=user_name)
        # 总时长
        total_online_time = all_online_time.aggregate(sum=Sum("online_time"))["sum"] or 0

        return all_online_time, total_online_time


class AppUseRecordManager(models.Manager):
    """
    用户使用APP记录操作
    """

    def save_app_use_record(self, user, app_id, access_host, source_ip):
        """
        保存App访问记录
        app_id：app的真实ID
        return：0：保存失败，1：保存成功
        """
        try:
            app = App.objects.get(id=app_id)
            self.model(user=user, app=app, access_host=access_host, source_ip=source_ip).save()
            return True
        except Exception as error:
            logger.error("An error occurred while saving App use records：%s" % error)
            return False

    def get_appuserecord(self, stime, etime, app_code):
        """
        获取经过过滤的app使用记录数据
        """
        all_visit = self.filter()
        if stime:
            all_visit = all_visit.filter(use_time__gte=stime)
        if etime:
            oneday = datetime.timedelta(days=1)
            all_visit = all_visit.filter(use_time__lt=etime + oneday)
        # 筛选
        if app_code:
            all_visit = all_visit.filter(app__code=app_code)

        # 总访问量
        total_visit = all_visit.count()

        return all_visit, total_visit


class AppLivenessManager(models.Manager):
    def get_appliveness(self, stime, etime, app_code):
        """
        获取经过过滤的活跃度记录数据
        """
        all_liveness = self.filter(add_date__gte=stime, add_date__lte=etime)
        # 筛选
        if stime:
            all_liveness = all_liveness.filter(add_date__gte=stime)
        if etime:
            all_liveness = all_liveness.filter(add_date__lte=etime)
        if app_code:
            all_liveness = all_liveness.filter(app__code=app_code)

        # 总活跃度
        total_liveness = all_liveness.aggregate(sum=Sum("hits"))["sum"] or 0

        return all_liveness, total_liveness
