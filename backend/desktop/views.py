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
from builtins import str

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import translation

from app.constants import OpenModeEnum
from app.models import App
from common.constants import DESKTOP_DEFAULT_APP_HEIGHT, DESKTOP_DEFAULT_APP_WIDTH
from common.exceptions import ConsoleErrorCodes
from common.log import logger
from desktop.constants import DEFALUT_FOLDER_ICO
from desktop.models import UserApp, UserSettings, Wallpaper
from desktop.utils import get_app_logo_url


def index(request):
    """
    桌面首页
    """
    return render(request, "desktop/index.html")


def desk_setting(request):
    """
    桌面(应用码头)设置页面
    """
    try:
        # 查询目前的桌面设置
        user_settings = UserSettings.objects.get(user=request.user)
        # 码头位置为空则使用默认值'left'
        dockpos = user_settings.dockpos if user_settings.dockpos else "left"
        appxy = user_settings.appxy if user_settings.appxy else "y"
        ctx = {"dockpos": dockpos, "appxy": appxy}
    except UserSettings.DoesNotExist:
        ctx = {"dockpos": "left", "appxy": "y"}
    return render(request, "desktop/desk_setting.html", ctx)


def get_appxy(request):
    """
    获得图标(APP)排列方式
    """
    try:
        # 查询用户的排列方式设置,如果为空，则使用默认值
        user_settings = UserSettings.objects.get(user=request.user)
        # app排列方式为空则使用默认值'y'
        appxy = user_settings.appxy if user_settings.appxy else "y"
    except UserSettings.DoesNotExist:
        appxy = "y"
    return HttpResponse(appxy)


def set_appxy(request, xy):
    """
    更新图标排列方式
    xy: APP的排列方式(x, y)
    """
    # 保存用户图标排列方式
    UserSettings.objects.update_user_appxy(request.user, xy)
    return HttpResponse()


def get_dock_pos(request):
    """
    获得应用码头位置
    """
    try:
        # 查询用户的应用码头位置设置,如果为空，则使用默认值
        user_settings = UserSettings.objects.get(user=request.user)
        # 码头位置为空则使用默认值'left'
        dockpos = user_settings.dockpos if user_settings.dockpos else "left"
    except UserSettings.DoesNotExist:
        dockpos = "left"
    return HttpResponse(dockpos)


def set_dock_pos(request, pos):
    """
    更新应用码头位置
    pos: 应用码头的位置（top,left,right）
    """
    # 保存用户码头设置
    UserSettings.objects.update_user_dock_pos(request.user, pos)
    return HttpResponse(pos)


def wallpaper(request):
    """
    设置壁纸首页
    """
    # 获取默认壁纸
    wallpaper_id_default = Wallpaper.objects.get_default_wallpaper()
    wallpaper_type_default = "lashen"
    # 查询目前的壁纸设置
    try:
        user_settings = UserSettings.objects.get(user=request.user)
        wallpaper_id = user_settings.wallpaper_id if user_settings.wallpaper_id else wallpaper_id_default
        wallpaper_type = user_settings.wallpaper_type if user_settings.wallpaper_type else wallpaper_type_default
    except UserSettings.DoesNotExist:
        wallpaper_id = wallpaper_id_default
        wallpaper_type = wallpaper_type_default
    # 获取壁纸总个数
    all_wallpaper = Wallpaper.objects.all()
    wall_list = [{"id": i.number, "name": i.name} for i in all_wallpaper]
    ctx = {
        "wallpaper_id": wallpaper_id,  # 用户使用的壁纸id
        "wallpaper_type": wallpaper_type,  # 用户壁纸显示方式
        "wall_list": wall_list,
    }
    return render(request, "desktop/wallpaper.html", ctx)


def get_wallpaper(request):
    """
    获得壁纸
    """
    # 获取默认壁纸
    wallpaper_id_default = Wallpaper.objects.get_default_wallpaper()
    wallpaper_type_default = "lashen"
    try:
        # 查询用户的壁纸信息,如果为空，则使用默认值
        try:
            user_settings = UserSettings.objects.get(user=request.user)
            wallpaper_id = user_settings.wallpaper_id if user_settings.wallpaper_id else wallpaper_id_default
            wallpaper_type = user_settings.wallpaper_type if user_settings.wallpaper_type else wallpaper_type_default
        except UserSettings.DoesNotExist:
            wallpaper_id = wallpaper_id_default
            wallpaper_type = wallpaper_type_default
        if not Wallpaper.objects.filter(number=wallpaper_id).exists():
            wallpaper_id = wallpaper_id_default
            wallpaper_type = wallpaper_type_default
        # 获取壁纸详细设置信息并组装数据
        user_wp = Wallpaper.objects.get(number=wallpaper_id)
        wp_url = settings.STATIC_URL + "img/wallpaper/wallpaper%s.jpg" % wallpaper_id
        wallpaper = "1<{|}>%s<{|}>%s<{|}>%d<{|}>%d" % (wp_url, wallpaper_type, user_wp.width, user_wp.height)
    except Exception as error:
        logger.error("An error occurred in getting wallpaper, Error message: %s" % error)
        wallpaper = "1<{|}>" + settings.STATIC_URL + "img/wallpaper/wallpaper1.jpg<{|}>lashen<{|}>1920<{|}>1080"  # 默认值
    return HttpResponse(wallpaper)


def set_wallpaper(request):
    """
    设置壁纸
    """
    # 选择的壁纸(1,2,3,4,5,6,7,8...)
    wp = request.POST.get("wp", "")
    # 壁纸的显示方式(tianchong,lashen...)
    wptype = request.POST.get("wptype", "lashen")
    # 修改wallpaper的设置, note:如果wp为空，则表示不修改该属性
    UserSettings.objects.update_user_wallpaper(request.user, wp, wptype)
    return HttpResponse()


def skin(request):
    """
    窗口皮肤设置首页
    """
    try:
        # 查询目前的皮肤设置, 并修改模版页面
        user_settings = UserSettings.objects.get(user=request.user)
        # 窗口皮肤为空则为默认设置'mac'
        user_skin = user_settings.skin if user_settings.skin else "mac"
        ctx = {"skin": user_skin}
    except UserSettings.DoesNotExist:
        ctx = {"skin": "mac"}
    return render(request, "desktop/skin.html", ctx)


def get_skin(request):
    """
    获得窗口皮肤
    """
    try:
        # 查询目前的皮肤设置, 并修改模版页面
        user_settings = UserSettings.objects.get(user=request.user)
        # 窗口皮肤为空则为默认设置'mac'
        user_skin = user_settings.skin if user_settings.skin else "mac"
    except UserSettings.DoesNotExist:
        user_skin = "mac"
    return HttpResponse(user_skin)


def set_skin(request, skin):
    """
    设置窗口皮肤
    skin: 选择的皮肤(default, mac, chrom, ext...)
    """
    # 保存用户窗口皮肤设置
    UserSettings.objects.update_user_skin(request.user, skin)
    return HttpResponse()


def get_my_app(request):
    """
    获得桌面图标(APP)，不做app类型和状态过滤
    """
    user = request.user
    # 初始化桌面
    pos = {"dock": [], "desk1": [], "desk2": [], "desk3": [], "desk4": [], "desk5": [], "folder": []}
    # 桌面
    desk_list = ["desk1", "desk2", "desk3", "desk4", "desk5"]
    # 用户初次登录时， user_settings中插入用户记录
    UserSettings.objects.init_user_settings(user)
    # 获取用户各桌面应用（不做过滤）

    user_app_dict, user_app_set, folder_dict = UserApp.objects.get_user_desktop_app_info(user=user)

    # 根据user_settings查询desk下的app
    try:
        user_settings = UserSettings.objects.filter(user=user).values("desk1", "desk2", "desk3", "desk4", "desk5")
        user_settings = user_settings[0]
        for desk in desk_list:
            # 查询该desk下该用户的所有app详细信息
            if user_settings[desk]:
                # 桌面user_app id 列表
                desk_app_id_list = user_settings[desk].split(",")
                # 查找该桌面的app列表
                for app_id in desk_app_id_list:
                    # 查询app信息
                    if app_id and int(app_id) in user_app_set:
                        # app信息
                        _user_app = user_app_dict[int(app_id)]
                        # 用户桌面应用数据组装（根据user_settings里对应桌面my_app_id列表排序），在文件夹的应用不显示在桌面
                        if not _user_app["parentid"]:
                            pos[desk].append(_user_app)
    except Exception as error:
        error_message = "%s, Failed to assemble user desktop app data, Username: %s, Error message: %s" % (
            ConsoleErrorCodes.E1303100_DESKTOP_USER_APP_LOAD_ERROR,
            user.username,
            error,
        )
        logger.error(error_message)

    # 根据folder_id查询每个文件夹下的app
    pos["folder"] = [{"appid": i, "apps": folder_dict[i]} for i in folder_dict]

    return JsonResponse(pos)


def get_my_app_by_id(request, app_id):
    """
    通过APP_id获得图标(APP)
    app_id: user_app_id(通过应用市场打开应用时，appid为应用真实的id，需要区分)
    """
    user = request.user
    try:
        user_app = UserApp.objects.get(user=user, id=app_id)
        desk_app_type = user_app.desk_app_type  # 用户app的类型（0：app，1：folder）
        # folder
        if desk_app_type == 1:
            # 查询folder的相关信息
            app_info = {
                "appid": app_id,
                "type": "folder",
                "realappid": 0,
                "app_code": "",
                "name": user_app.folder_name,
                "icon": DEFALUT_FOLDER_ICO,
                "width": 650,  # 固定
                "height": 400,  # 固定
                "isresize": 0,
                "isopenmax": 0,
                "issetbar": 0,
                "url": "",
                "is_outline": 0,
                "islapp": 0,
                "open_mode": OpenModeEnum.DESKTOP,
            }
        else:
            # 查询APP的基本信息
            app = user_app.app
            is_en = translation.get_language() == "en"
            app_name = app.name_display
            if is_en:
                app_name = app.name_en_display or app.code

            app_info = {
                "appid": app_id,
                "type": "app",
                "realappid": app.id,
                "app_code": app.code,
                "name": app_name,
                "icon": get_app_logo_url(app.code),
                "width": app.width or DESKTOP_DEFAULT_APP_WIDTH,
                "height": app.height or DESKTOP_DEFAULT_APP_HEIGHT,
                "isresize": 1 if app.is_resize else 0,
                "isopenmax": 1 if app.is_max else 0,
                "issetbar": 1 if app.is_setbar else 0,
                "isthird": 1 if app.is_third else 0,
                "url": app.app_pro_url,
                "is_outline": 0 if app.state > 0 and app.is_already_online else 1,
                "islapp": 1 if app.is_lapp else 0,
                "open_mode": app.open_mode,
                "is_in_paas3": 1 if app.is_in_paas3 else 0,
            }
    except Exception as error:
        logger.error("Failed to get app info via app_id, User_app_id：%s, Error message: %s" % (app_id, error))
        app_info = {"error": "E100"}  # E100  应用不存在的错误编码
    return JsonResponse(app_info)


def get_my_app_by_code(request, app_code):
    """
    通过app code获取app详细信息
    """
    user = request.user
    try:
        # 获取app基本信息
        app = App.objects.get(code=app_code)
        # 应用已经下架、开发中，打开给错误提示
        if app.state == 0:
            app_info = {"error": "E200"}  # 应用已经下架
        elif app.state == 1 or (app.state > 0 and not app.is_already_online):
            app_info = {"error": "E300"}  # 应用未提测
        else:
            # 查询APP的基本信息
            user_app = UserApp.objects.filter(user=user, app=app)

            is_en = translation.get_language() == "en"
            app_name = app.name_display
            if is_en:
                app_name = app.name_en_display or app_code

            # 获取基本信息
            app_info = {
                "appid": user_app[0].id if user_app else "",
                "type": "app",
                "realappid": app.id,
                "app_code": app_code,
                "name": app_name,
                "icon": get_app_logo_url(app.code),
                "width": app.width or DESKTOP_DEFAULT_APP_WIDTH,
                "height": app.height or DESKTOP_DEFAULT_APP_HEIGHT,
                "isresize": 1 if app.is_resize else 0,
                "isopenmax": 1 if app.is_max else 0,
                "issetbar": 1 if app.is_setbar else 0,
                "isthird": 1 if app.is_third else 0,
                "url": app.app_pro_url,
                "is_outline": 0 if app.state > 0 and app.is_already_online else 1,
                "islapp": 1 if app.is_lapp else 0,
                "return_code": 1 if user_app else 0,  # 1:已经添加，0：未添加
                "open_mode": app.open_mode,
                "is_in_paas3": 1 if app.is_in_paas3 else 0,
            }
    except Exception as error:
        logger.error("Failed to get app info via app_code, App_code：%s, Error message: %s" % (app_code, error))
        app_info = {"error": "E100"}  # E100  应用不存在的错误编码

    return JsonResponse(app_info)


def add_folder(request):
    """
    添加文件夹
    """
    name = request.POST.get("name")
    desk = "desk%s" % request.POST.get("desk", "1")
    # 存储文件夹信息
    return_code = UserApp.objects.add_folder(request.user, name, desk)
    # response返回状态码
    return HttpResponse(str(return_code))


def update_folder(request, app_id):
    """
    文件夹重命名
    app_id: 文件夹对应的user_app表id
    """
    name = request.POST.get("name")
    # 更新文件夹名称
    return_code = UserApp.objects.update_folder_name(request.user, app_id, name)
    return HttpResponse(str(return_code))


def add_my_app(request, app_id):
    """
    添加桌面图标
    """
    desk = "desk%s" % request.POST.get("desk", "1")
    try:
        return_code = 0
        # 判断要添加的应用是否为存在
        if App.objects.filter(id=int(app_id)).exists():
            # 把app添加到桌面 insert into user_app
            return_code = UserApp.objects.add_app(request.user, desk, app_id)
    except Exception as error:
        logger.error("Add app failed, Error message: %s" % error)
        return_code = 0
    return HttpResponse(str(return_code))


def del_my_app(request, my_app_id):
    """
    删除桌面图标
    """
    # delete from user_app
    return_code = UserApp.objects.del_app(request.user, my_app_id)
    return HttpResponse(str(return_code))


def move_my_app(request, my_app_id):
    """
    移动桌面图标到另一个桌面
    """
    fromdesk = request.POST.get("fromdesk", "")  # app移出的桌面
    todesk = "desk%s" % request.POST.get("todesk")  # app移入的桌面
    fromfolder = request.POST.get("fromfolder", "")  # 用于判断是否从文件夹点击右键移动app到桌面, 值为folder对应的id
    if fromdesk:
        fromdesk = "desk%s" % fromdesk
    # 修改app_position并更新setting
    return_code = UserApp.objects.move_my_app(request.user, my_app_id, fromdesk, todesk, fromfolder)
    return HttpResponse(str(return_code))


def update_my_app(request, my_app_id):
    """
    更新桌面图标
    """
    move_type = request.POST.get("movetype")  # 移动类型
    _from = request.POST.get("from")  # 原来的位置(从0开始)
    _to = request.POST.get("to")  # 拖到的位置(从0开始)
    desk = "desk%s" % request.POST.get("desk")  # 应用初始所在desk
    otherdesk = "desk%s" % request.POST.get("otherdesk")  # 应用最终所在desk
    user = request.user  # 用户
    return_code = 1  # 默认值

    if move_type == "desk-folder":
        # 应用从桌面添加到文件夹
        return_code = UserApp.objects.my_app_desk_folder(user, my_app_id, desk, _to)
    elif move_type == "desk-desk":
        # 从同桌面一个位置拖动到另一个位置
        return_code = UserSettings.objects.my_app_desk_desk(user, my_app_id, desk, _from, _to)
    elif move_type == "desk-otherdesk":
        # 应用从桌面添加到另一个桌面
        return_code = UserApp.objects.my_app_desk_otherdesk(user, my_app_id, desk, otherdesk, _from, _to)
    elif move_type == "folder-otherfolder":
        # 应用从一个文件夹添加到另一个文件夹
        return_code = UserApp.objects.my_app_folder_otherfolder(user, my_app_id, _to)
    elif move_type == "folder-desk":
        # 应用从文件夹移动到桌面
        return_code = UserApp.objects.my_app_folder_desk(user, my_app_id, desk, _to)

    return HttpResponse(str(return_code))


def is_user_added_app(request, app_code):
    """
    判断用户是否添加了该应用（未添加返回false,app真实id）
    app_code: app编码
    """
    try:
        if UserApp.objects.filter(app__code=app_code, user=request.user).exists():
            result = {"result": True, "realappid": ""}
        else:
            app = App.objects.get(code=app_code)
            # 应用已经下架、开发中，打开给错误提示
            if app.state == 0:
                result = {"error": "E200"}  # 应用已下架
            elif app.state == 1 or (app.state > 0 and not app.is_already_online):
                result = {"error": "E300"}  # 应用未提测
            else:
                result = {"result": False, "realappid": app.id}
    except Exception as error:
        logger.error("Determine whether the user have added the app, Error message: %s" % error)
        result = {"error": "E100"}
    # 返回
    return JsonResponse(result)


def search_apps(request):
    """
    桌面搜索应用
    """
    try:
        search = request.GET.get("search", "")
        all_app = []
        if search:
            # 所有应用（过滤已下架应用（state=0）、开发中应用（state=1））
            all_app = App.objects.filter(state__gt=1, is_already_online=True)
            # 组装搜索框中多个搜索条件
            all_app = all_app.filter(
                Q(code__icontains=search)
                | Q(name__icontains=search)
                | Q(developer__username__icontains=search)
                | Q(developer__chname__icontains=search)
            )
        apps = [{"name": i.name_display, "code": i.code, "type": "app", "appid": 0} for i in all_app]
    except Exception as error:
        logger.error("An error occurred in desktop search for apps, error：%s" % error)
        apps = []
    return JsonResponse({"apps": apps})
