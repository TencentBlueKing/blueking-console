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
from django.conf.urls import url

from common.constants import CODE_REGEX
from desktop import market_views, other_views, views

# web桌面设置
urlpatterns = [
    # 首页
    url(r"^$", views.index),
    # 首次登陆（用于首次引导）
    # url(r'^is_login_first/$', views.is_login_first),                                       # 判断用户是否首次登录系统
    # url(r'^set_login_first/$', views.set_login_first),                                     # 标记用户非第一次登录
    # 桌面（应用码头）设置
    url(r"^desk_setting/$", views.desk_setting),  # 桌面(应用码头)设置页面
    # app排列方式（横排或竖排）
    url(r"^get_appxy/$", views.get_appxy),  # 获取APP排列方式
    url(r"^set_appxy/(?P<xy>\w+)/$", views.set_appxy),  # 设置APP排列方式
    # 应用码头位置（左、上、右）
    url(r"^get_dock_pos/$", views.get_dock_pos),  # 获取应用码头位置
    url(r"^set_dock_pos/(?P<pos>\w+)/$", views.set_dock_pos),  # 更新应用码头位置
    # 桌面壁纸
    url(r"^wallpaper/$", views.wallpaper),  # 设置壁纸首页
    url(r"^get_wallpaper/$", views.get_wallpaper),  # 获得壁纸
    url(r"^set_wallpaper/$", views.set_wallpaper),  # 更新壁纸
    # 窗口皮肤
    url(r"^skin/$", views.skin),  # 窗口皮肤设置首页
    url(r"^get_skin/$", views.get_skin),  # 获得窗口皮肤
    url(r"^set_skin/(?P<skin>\w+)/$", views.set_skin),  # 更新窗口皮肤
]

# 企业版版本和许可证相关
urlpatterns += [
    # 获取许可证提示信息
    url(r"^get_license_notice/$", other_views.get_license_notice),
    # 获取版本信息
    url(r"^get_version_info/$", other_views.get_version_info),
]

# 桌面app管理
urlpatterns += [
    # 查询APP信息
    url(r"^get_my_app/$", views.get_my_app),  # 获取用户桌面应用
    url(r"^get_my_app_by_id/(?P<app_id>\d+)/$", views.get_my_app_by_id),  # 通过app_id获得APP信息
    url(r"^get_my_app_by_code/(?P<app_code>" + CODE_REGEX + ")/$", views.get_my_app_by_code),  # 通过app_code获得APP信息
    # 文件夹
    url(r"^add_folder/$", views.add_folder),  # 新建文件夹
    url(r"^update_folder/(?P<app_id>\d+)/$", views.update_folder),  # 文件夹重命名
    # 移动和添加app
    url(r"^add_my_app/(?P<app_id>\d+)/$", views.add_my_app),  # 添加桌面应用
    url(r"^del_my_app/(?P<my_app_id>\d+)/$", views.del_my_app),  # 删除桌面应用
    url(r"^move_my_app/(?P<my_app_id>\d+)/$", views.move_my_app),  # 移动桌面应用到另一个桌面
    url(r"^update_my_app/(?P<my_app_id>\d+)/$", views.update_my_app),  # 更新桌面应用
    url(r"^is_user_added_app/(?P<app_code>" + CODE_REGEX + ")/$", views.is_user_added_app),  # 判断用户是否添加了该app
    # 搜索应用
    url(r"^search_apps/$", views.search_apps),  # 搜索应用
]

# 应用市场
urlpatterns += [
    url(r"^market/$", market_views.market),  # 应用市场首页
    url(r"^set_market_nav/$", market_views.set_market_nav),  # 设置应用市场左侧导航
    url(r"^market_get_list/$", market_views.market_get_list),  # 应用市场APP查询（分页查询）
    url(r"^market_app_detail/(?P<app_id>\d+)/$", market_views.market_app_detail),  # 应用市场APP详细信息
    url(r"^market_get_nearest_open_app/$", market_views.market_get_nearest_open_app),  # 应用市场最近打开的应用
    url(r"^update_app_star/(?P<app_id>\d+)/$", market_views.update_app_star),  # 应用评分
]
