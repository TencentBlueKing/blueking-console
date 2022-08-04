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

from django.db import models, transaction
from django.db.models import F
from django.utils import translation

from common.log import logger
from desktop.constants import DEFALUT_FOLDER_ICO, MarketNavEnum
from desktop.utils import get_app_logo_url


class WallpaperManager(models.Manager):
    """
    壁纸管理
    """

    def get_default_wallpaper(self):
        """
        获取默认壁纸
        """
        # 默认壁纸
        try:
            wallpaper_id = 1
            default_paper = self.filter(is_default=True)
            if default_paper:
                wallpaper_id = default_paper[0].number
        except Exception as error:
            logger.error("Get default wallpaper failed！Error message: %s" % error)
            wallpaper_id = 1
        return wallpaper_id


class UserSettingsManager(models.Manager):
    """
    用户桌面设置操作
    """

    def get_user_market_nav(self, username):
        """
        获取用户桌面应用市场左侧导航类别
        """
        try:
            return self.get(user__username=username).market_nav
        except Exception:
            return MarketNavEnum.APPTAG

    def update_user_market_nav(self, user, market_nav):
        """
        更新用户桌面应用市场左侧导航类别
        """
        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新，不存在则保存新用户数据）
            if user_set:
                user_set.update(market_nav=market_nav)
            else:
                self.model(user=user, market_nav=market_nav).save()
            return True
        except Exception as error:
            logger.error(
                "Category setting in the left navigation of user's desktop app market failed, Error message：%s" % error
            )
            return False

    def update_user_appxy(self, user, appxy):
        """
        保存用户桌面app排列方式
        appxy: app设置的排列方式
        """
        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新桌面app排列方式，不存在则保存新用户数据）
            if user_set:
                user_set.update(appxy=appxy)
            else:
                self.model(user=user, appxy=appxy).save()
            return True
        except Exception as error:
            logger.error("The arrangement mode of app setting failed, Error message: %s" % error)
            return False

    def update_user_dock_pos(self, user, dockpos):
        """
        保存用户桌面码头设置
        dockpos: 用户设置的码头位置
        """
        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新桌面设置信息，不存在则保存新用户数据）
            if user_set:
                user_set.update(dockpos=dockpos)
            else:
                self.model(user=user, dockpos=dockpos).save()
            return True
        except Exception as error:
            logger.error("Dock position setting failed, Error message: %s" % error)
            return False

    def update_user_wallpaper(self, user, wp, wptype):
        """
        保存用户壁纸设置
        wp:用户设置的壁纸
        wptype: 用户设置的壁纸 显示方式
        """
        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新用户壁纸设置，不存在则保存新用户数据）
            if user_set:
                if wp:
                    user_set.update(wallpaper_type=wptype, wallpaper_id=wp)
                else:
                    user_set.update(wallpaper_type=wptype)
            else:
                wp = 1 if not wp else wp
                self.model(user=user, wallpaper_type=wptype, wallpaper_id=wp).save()
            return True
        except Exception as error:
            logger.error("User wallpaper setting failed, Error message: %s" % error)
            return False

    def update_user_skin(self, user, skin):
        """
        保存用户窗口皮肤设置
        skin: 用户设置的皮肤设置
        """
        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新用户窗口皮肤设置，不存在则保存新用户数据）
            if user_set:
                user_set.update(skin=skin)
            else:
                self.model(user=user, skin=skin).save()
            return True
        except Exception as error:
            logger.error("Window skin setting failed, Error message: %s" % error)
            return False

    def init_user_settings(self, user):
        """
        初始化用户设置
        """
        from app.models import App
        from desktop.models import UserApp, Wallpaper

        try:
            user_set = self.filter(user=user)
            # 判断用户设置信息是否存在（存在则更新用户设置，不存在则保存新用户数据）
            if not user_set:
                # 获取默认的壁纸
                wallpaper_id_default = Wallpaper.objects.get_default_wallpaper()
                wallpaper_type_default = "lashen"
                self.model(user=user, wallpaper_id=wallpaper_id_default, wallpaper_type=wallpaper_type_default).save()
                # 将（已上线）默认应用添加到用户桌面
                default_app = App.objects.filter(is_already_online=True, state__gt=1, is_default=True).values_list(
                    "id", flat=True
                )
                for app_id in default_app:
                    UserApp.objects.add_app(user, "desk1", app_id)
            return True
        except Exception as error:
            logger.error("Initialization of user settings failed, Error message: %s" % error)
            return False

    def _update_user_settings_by_desk(self, desk, app_id_list, user_set):
        """
        更新用户设置时，根据desk判断更新字段
        """
        # 判断应用更新哪个桌面的数据
        if desk == "dock":
            user_set.update(dock=app_id_list)
        elif desk == "desk1":
            user_set.update(desk1=app_id_list)
        elif desk == "desk2":
            user_set.update(desk2=app_id_list)
        elif desk == "desk3":
            user_set.update(desk3=app_id_list)
        elif desk == "desk4":
            user_set.update(desk4=app_id_list)
        elif desk == "desk5":
            user_set.update(desk5=app_id_list)

    def update_user_settings_desk(self, user, desk, my_app_id, operate_type):
        """
        添加应用或文件夹时 更新或添加用户桌面app信息设置
        desk：文件夹或app要添加的desk
        user_app_id: 应用或文件夹对应的user_app_id
        operate_type: 0: 添加文件夹或app, 1: 删除app或文件夹
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                # 添加app或文件夹
                if operate_type == 0:
                    is_update = True
                    desk_appid = user_set[0][desk]  # desk对应的appid字符串
                    if desk_appid:
                        # 判断app是否已经添加到该桌面appid list里
                        _desk_appid_list = desk_appid.split(",")
                        if str(my_app_id) not in _desk_appid_list:
                            app_id_list = "%s,%s" % (desk_appid, my_app_id)
                        else:
                            app_id_list = desk_appid
                    else:
                        app_id_list = "%s" % my_app_id
                # 删除app或文件夹
                elif operate_type == 1:
                    is_update = False
                    # 查找app或文件夹所在desk
                    for desk in user_set[0]:
                        desk_app_id_list = user_set[0][desk].split(",") if user_set[0][desk] else []
                        # 删除app id
                        if str(my_app_id) in desk_app_id_list:
                            desk_app_id_list.remove(str(my_app_id))
                            app_id_list = ",".join(desk_app_id_list)
                            is_update = True
                            break
                # 更新user_settings
                if is_update:
                    self._update_user_settings_by_desk(desk, app_id_list, user_set)
                return 1  # 成功返回码
            else:
                return 0  # 失败返回码
        except Exception as error:
            msg = (
                "Updating or adding user desktop app information settings when adding an app or folder failed, "
                "Operate_type: %s, Error message: %s"
            ) % (operate_type, error)
            logger.error(msg)
            return 0  # 失败返回码

    def move_my_app_update(self, user, my_app_id, fromdesk, todesk, fromfolder):
        """
        移动桌面图标到另一个桌面,更新桌面顺序
        my_app_id: 移动的app对应的user_app_id
        fromdesk: app最初所在desk
        todesk: app最终所在desk
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                # 从桌面移动
                if fromdesk:
                    # 获取app最初所在desk的appid列表
                    from_desk_app_id = user_set[0][fromdesk].split(",") if user_set[0][fromdesk] else []
                    # 删除该app 的id（该应用不在该桌面，则桌面app不变）
                    from_desk_app_id.remove(str(my_app_id))
                    # 更新User_settings有关该桌面的数据
                    self._update_user_settings_by_desk(fromdesk, ",".join(from_desk_app_id), user_set)
                todesk_appid = user_set[0][todesk]
                # 获取app最终所在desk的app_id 列表  ，添加该应用id在最末
                if todesk_appid:
                    # 判断app是否已经添加到该桌面appid list里
                    _todesk_appid_list = todesk_appid.split(",")
                    if str(my_app_id) not in _todesk_appid_list:
                        to_desk_app_id = "%s,%s" % (todesk_appid, my_app_id)
                    else:
                        to_desk_app_id = todesk_appid
                else:
                    to_desk_app_id = "%s" % (my_app_id)
                # 更新User_settings中todesk的数据
                self._update_user_settings_by_desk(todesk, to_desk_app_id, user_set)
                return 1  # 成功返回码
            return 0  # 失败返回码
        except Exception as error:
            logger.error("Failed to move the icon from one desktop to another, Error message: %s" % error)
            return 0  # 失败返回码

    def my_app_desk_folder(self, user, my_app_id, desk):
        """
        将桌面app移到文件夹内
        my_app_id: 移动的app对应的user_app_id
        desk: app所在desk
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                # 获取该桌面的appidlist
                desk_app_id_list = user_set[0][desk].split(",") if user_set[0][desk] else []
                # 删除该user_seetings里该app的user_app_id
                desk_app_id_list.remove(str(my_app_id))
                # 更新user_settings
                self._update_user_settings_by_desk(desk, ",".join(desk_app_id_list), user_set)
                return 1  # 成功返回码
            return 0  # 失败返回码
        except Exception as error:
            logger.error("Failed to move the desktop app to the folder, Error message: %s" % error)
            return 0  # 失败返回码

    def my_app_desk_desk(self, user, my_app_id, desk, _from, _to):
        """
        从同一个桌面一个位置拖动到另一个位置
        my_app_id: 移动的app对应的user_app_id
        desk: app所在desk
        _from: app最出所在位置
        _to: app最终所在位置
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                # 获取该桌面的appidlist
                desk_app_id_list = user_set[0][desk].split(",") if user_set[0][desk] else []
                # 获取my_app_id所在的位置
                index = desk_app_id_list.index(str(my_app_id))
                # 将appid插入到_to的位置，并从原来位置移除
                desk_app_id_list.pop(index)
                desk_app_id_list.insert(int(_to), my_app_id)
                # 更新user_settings
                self._update_user_settings_by_desk(desk, ",".join(desk_app_id_list), user_set)
                return 1  # 成功返回码
            else:
                return 0  # 失败返回码
        except Exception as error:
            logger.error("Failed to drag from one location to another on the same desktop, Error message: %s" % error)
            return 0  # 失败返回码

    def my_app_desk_otherdesk(self, user, my_app_id, desk, otherdesk, _from, _to):
        """
        将桌面app移到另一个桌面
        my_app_id: 移动的app对应的user_app_id
        desk: app最初所在desk
        otherdesk: app最终所在desk
        _from: app最初所在desk的位置
        _to: app最终所在desk的位置
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                # 获取最初所在桌面的appid列表
                desk_app_id_list = user_set[0][desk].split(",") if user_set[0][desk] else []
                # 删除该user_seetings里该app的user_app_id
                desk_app_id_list.remove(str(my_app_id))
                # 更新user_settings
                self._update_user_settings_by_desk(desk, ",".join(desk_app_id_list), user_set)
                otherdesk_appid = user_set[0][otherdesk]
                # 获取最终所在桌面的appid列表(判断该桌面是否有app)
                if otherdesk_appid:
                    # 判断app是否已经添加到该桌面appid list里
                    other_desk_app_id_list = otherdesk_appid.split(",")
                    if str(my_app_id) not in other_desk_app_id_list:
                        # user_seetings里insert该app的user_app_id
                        other_desk_app_id_list.insert(int(_to), my_app_id)
                else:
                    other_desk_app_id_list = [my_app_id]
                # 更新user_settings
                self._update_user_settings_by_desk(otherdesk, ",".join(other_desk_app_id_list), user_set)
                return 1  # 成功返回码
            else:
                return 0  # 失败返回码
        except Exception as error:
            logger.error("Failed to move an app from one desktop to another, Error message: %s" % error)
            return 0  # 失败返回码

    def my_app_folder_desk(self, user, my_app_id, desk, _to):
        """
        将文件夹app移到桌面
        my_app_id: 移动的app对应的user_app_id
        desk: app要移入所在desk
        _to: app要移入desk的位置
        return: 0:user_settings更新失败，1：user_settings更新成功
        """
        try:
            # 获取该用户各桌面的appid列表
            user_set = self.filter(user=user).values("dock", "desk1", "desk2", "desk3", "desk4", "desk5")
            if user_set:
                desk_appid = user_set[0][desk]
                # 获取最终所在桌面的appid列表(判断该桌面是否有app)
                if desk_appid:
                    # 判断app是否已经添加到该桌面appid list里
                    desk_app_id_list = desk_appid.split(",")
                    if str(my_app_id) not in desk_app_id_list:
                        # user_seetings里插入该app的user_app_id
                        desk_app_id_list.insert(int(_to), my_app_id)
                else:
                    desk_app_id_list = [my_app_id]
                # 更新user_settings
                self._update_user_settings_by_desk(desk, ",".join(desk_app_id_list), user_set)
                return 1  # 成功返回码
            else:
                return 0  # 失败返回码
        except Exception as error:
            logger.error("Failed to move folder app to desktop, Error message: %s" % error)
            return 0  # 失败返回码


class UserAppManager(models.Manager):
    """
    用户桌面应用、文件夹操作
    """

    def add_folder(self, user, folder_name, desk):
        """
        添加文件夹
        folder_name: 新文件夹名称
        desk: 文件夹所在桌面
        return: 0:文件夹添加失败，1：文件夹添加成功，2：文件夹重名
        """
        from desktop.models import UserSettings

        # 查询该文件夹名对应folder
        _folder = self.filter(user=user, desk_app_type=1, folder_name=folder_name)
        # 判断floder 名是否存在（存在则返回重名码2）
        if not _folder:
            retrun_code = 0
            try:
                with transaction.atomic():
                    # 创建新的folder
                    new_folder = self.model(user=user, desk_app_type=1, folder_name=folder_name, app_position=desk)
                    new_folder.save()
                    # 更新 User_settings
                    UserSettings.objects.update_user_settings_desk(user, desk, new_folder.id, 0)
                    retrun_code = 1
            except Exception as error:
                logger.error("Failed to add folder, Error message: %s" % error)
                retrun_code = 0
            return retrun_code
        return 2  # 文件夹名重复

    def update_folder_name(self, user, app_id, folder_name):
        """
        更新文件夹名称
        app_id:更名的folder的id
        folder_name: 修改后的文件夹名
        return: 0:文件夹更名失败，1：文件夹更名成功，2：文件夹重名
        """
        # 查询该folder_name是否有相同名称的文件夹
        _folder_has = self.filter(user=user, desk_app_type=1, folder_name=folder_name).exclude(id=app_id)
        # 判断是否重名，重名返回2
        if not _folder_has:
            # 更新该文件夹的名称
            try:
                self.filter(user=user, desk_app_type=1, id=app_id).update(folder_name=folder_name)
                return 1  # 更名成功
            except Exception as error:
                logger.error("Failed to update folder name, Error message: %s" % error)
                return 0  # 出错
        else:
            return 2  # 文件夹名重复

    def add_app(self, user, desk, app_id):
        """
        添加应用（注意app use_count加1）
        desk: 应用要添加到的桌面
        app_id:app对应的id
        return: 0:app添加失败，1：app添加成功，2：用户已经添加了该应用
        """
        from app.models import App
        from desktop.models import UserSettings

        try:
            # 判断用户是否添加了该应用
            if self.filter(user=user, app__id=app_id):
                return 2  # 用户已经添加了应用的返回码
            return_code = 0
            with transaction.atomic():
                # 添加新的user_app数据
                new_app = self.model(app_id=app_id, user=user, desk_app_type=0, app_position=desk)
                new_app.save()
                # app use_count 加1
                App.objects.filter(id=app_id).update(use_count=F("use_count") + 1)
                # 更新 User_settings
                UserSettings.objects.update_user_settings_desk(user, desk, new_app.id, 0)
                return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to add an app in desktop, Error message: %s" % error)
            return_code = 0
        return return_code

    def del_app(self, user, app_id):
        """
        删除app(注意app usecount 减1)，分为删除app和删除folder
        app_id: 删除的app或文件夹对应的user_app_id
        return: 0:app或文件夹删除失败，1：app或文件夹删除成功，2：文件夹内有应用，不能删除，3：用户已经删除了该app或folder
        """
        from app.models import App
        from desktop.models import UserApp, UserSettings

        try:
            try:
                user_app = self.get(id=app_id, user=user)
            except UserApp.DoesNotExist:
                return 3  # 该应用或文件夹已经删除，返回状态码
            # 文件夹
            if user_app.desk_app_type == 1:
                # 删除folder(判断文件夹下是否有应用)
                if self.filter(parent=user_app, user=user, desk_app_type=0):
                    return 2  # 文件夹有应用时返回的状态码
            return_code = 0
            with transaction.atomic():
                if user_app.desk_app_type == 0:
                    # 删除app usecount 减1
                    App.objects.filter(id=user_app.app.id).update(use_count=F("use_count") - 1)
                # 删除user_setting数据
                UserSettings.objects.update_user_settings_desk(user, "", user_app.id, 1)
                # 删除用户app
                user_app.delete()
                return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to delete an app in desktop, Error message: %s" % error)
            return_code = 0  # 失败返回码
        return return_code

    def move_my_app(self, user, my_app_id, fromdesk, todesk, fromfolder):
        """
        移动桌面图标到另一个桌面
        fromdesk: app最初所在desk
        todesk: app最终所在desk
        my_app_id: app的 user_app_id
        return: 0:移动操作失败，1：移动操作成功
        """
        from desktop.models import UserSettings

        try:
            final_return_code = 0
            with transaction.atomic():
                # 更新user_settings
                return_code = UserSettings.objects.move_my_app_update(user, my_app_id, fromdesk, todesk, fromfolder)
                if return_code == 0:
                    # 更新user_settings失败
                    final_return_code = 0  # 失败返回码
                elif return_code == 1:
                    # 更新app的app_position
                    self.filter(user=user, id=my_app_id).update(app_position=todesk, parent=None)
                    final_return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to move desktop app to another desktop, Error message: %s" % error)
            final_return_code = 0
        return final_return_code

    def my_app_desk_folder(self, user, my_app_id, desk, _to):
        """
        将桌面应用移动到文件夹
        _to: app移入的文件夹的user_app_id
        my_app_id: app的 user_app_id
        desk: app所在desk
        return: 0:移动操作失败，1：移动操作成功
        """
        from desktop.models import UserSettings

        try:
            final_return_code = 0
            with transaction.atomic():
                # 更新user_setting
                return_code = UserSettings.objects.my_app_desk_folder(user, my_app_id, desk)
                if return_code == 0:
                    # 更新user_settings失败
                    final_return_code = 0  # 失败返回码
                elif return_code == 1:
                    # folder信息
                    folder = self.get(id=_to, user=user)
                    # 更新app的对应的parent
                    self.filter(user=user, id=my_app_id).update(parent=folder)
                    final_return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to move desktop app to folder, Error message: %s" % error)
            final_return_code = 0
        return final_return_code

    def my_app_desk_otherdesk(self, user, my_app_id, desk, otherdesk, _from, _to):
        """
        将桌面应用移动到另一个桌面
        _from: app移出的文件夹的user_app_id
        _to: app移入的文件夹的user_app_id
        my_app_id: app的 user_app_id
        desk: app最初所在desk
        otherdesk: app最终所在desk
        return: 0:移动操作失败，1：移动操作成功
        """
        from desktop.models import UserSettings

        try:
            final_return_code = 0
            with transaction.atomic():
                # 更新user_setting
                return_code = UserSettings.objects.my_app_desk_otherdesk(user, my_app_id, desk, otherdesk, _from, _to)
                if return_code == 0:
                    # 更新user_settings失败
                    final_return_code = 0  # 失败返回码
                elif return_code == 1:
                    # 更新app的user_app信息
                    self.filter(user=user, id=my_app_id).update(app_position=otherdesk)
                    final_return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to move desktop app to another desktop, Error message: %s" % error)
            final_return_code = 0
        return final_return_code

    def my_app_folder_otherfolder(self, user, my_app_id, _to):
        """
        将应用从一个文件夹移动到另一个文件夹
        _to: 移入的文件夹id
        my_app_id: app的 user_app_id
        return: 0:移动操作失败，1：移动操作成功
        """
        try:
            # 最终文件夹
            to_folder = self.get(id=_to)
            # 更新app的user_app信息（parent 改为 _to对应的文件夹）
            self.filter(user=user, id=my_app_id).update(parent=to_folder)
            return 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to move an app from one folder to another, Error message: %s" % error)
            return 0  # 出错返回码

    def my_app_folder_desk(self, user, my_app_id, desk, _to):
        """
        将文件夹应用移动到另一个桌面
        _to: app要移入的桌面位置
        my_app_id: app的 user_app_id
        desk: app要移入的所在desk
        return: 0:移动操作失败，1：移动操作成功
        """
        from desktop.models import UserSettings

        try:
            final_return_code = 0
            with transaction.atomic():
                # 更新user_settings
                return_code = UserSettings.objects.my_app_folder_desk(user, my_app_id, desk, _to)
                if return_code == 0:
                    # 更新user_settings失败
                    final_return_code = 0  # 失败返回码
                elif return_code == 1:
                    # 更新app的user_app信息
                    self.filter(user=user, id=my_app_id).update(app_position=desk, parent=None)
                    final_return_code = 1  # 成功返回码
        except Exception as error:
            logger.error("Failed to move the folder app to another desktop, Error message: %s" % error)
            final_return_code = 0
        return final_return_code

    def get_user_desktop_app_info(self, user):
        """
        获取用户各桌面应用（不做过滤）
        """
        folder_dict = {}
        user_app_dict = {}
        user_app_set = set()
        try:
            user_app_by_desk = (
                self.select_related("app", "user", "parent")
                .filter(user=user)
                .values(
                    "id",
                    "desk_app_type",
                    "app_position",
                    "folder_name",
                    "parent__id",
                    "app__name",
                    "app__name_en",
                    "app__code",
                    "app__id",
                    "app__state",
                    "app__is_lapp",
                )
            )

            is_en = translation.get_language() == "en"
            for user_app in user_app_by_desk:
                # 应用或文件夹信息
                if user_app["desk_app_type"] == 1:
                    app_icon = DEFALUT_FOLDER_ICO
                else:
                    app_icon = get_app_logo_url(user_app["app__code"])

                app_name = user_app["app__name"]
                if is_en:
                    app_name = user_app["app__name_en"] or user_app["app__name"]

                user_app_info = {
                    "appid": user_app["id"],
                    "type": "folder" if user_app["desk_app_type"] == 1 else "app",
                    "realappid": 0 if user_app["desk_app_type"] == 1 else user_app["app__id"],
                    "app_code": "" if user_app["desk_app_type"] == 1 else user_app["app__code"],
                    "name": user_app["folder_name"] if user_app["desk_app_type"] == 1 else app_name,  # noqa
                    "icon": app_icon,
                    "parentid": user_app["parent__id"],
                    "isoutline": "gray" if user_app["app__state"] == 0 else "",
                    "islapp": 1 if user_app["app__is_lapp"] else 0,
                }
                user_app_dict[user_app["id"]] = user_app_info
                user_app_set.add(user_app["id"])
                # 查看应用是否在文件夹中
                folder_id = user_app["parent__id"]
                if folder_id:
                    if folder_id not in folder_dict:
                        folder_dict[folder_id] = []
                    folder_dict[folder_id].append(user_app_info)

                # 文件夹
                if user_app["desk_app_type"] == 1:
                    if user_app["id"] not in folder_dict:
                        folder_dict[user_app["id"]] = []

        except Exception as error:
            logger.error("Get user desktop app failed, Username: %s, Error message: %s" % (user.username, error))
            user_app_dict = {}
        return user_app_dict, user_app_set, folder_dict
