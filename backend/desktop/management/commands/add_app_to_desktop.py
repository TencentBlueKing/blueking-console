import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db import models, transaction

from account.models import BkUser
from app.models import App
from desktop.models import UserApp, UserSettings, Wallpaper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--app_code', type=str, dest="app_code")
        parser.add_argument('--username', type=str, dest="username")

    def handle(self, app_code, username, *args, **option):
        try:
            user = BkUser.objects.get(username=username)
        except ObjectDoesNotExist:
            logger.error("user(%s) not exists" % username)
            return

        try:
            app = App.objects.get(code=app_code)
        except ObjectDoesNotExist:
            logger.error("App(%s) not exists" % app_code)
            return

        with transaction.atomic():
            _user_app, _user_app_create = UserApp.objects.get_or_create(
                user=user, app=app, defaults={'desk_app_type': 0, 'app_position': 'desk1'}
            )

            # 新添加的应用，则将使用数添加 1
            if _user_app_create:
                app.use_count = app.use_count + 1
                app.save()

            # 将应用添加到用户的桌面设置中
            user_setting, _c = UserSettings.objects.get_or_create(
                user=user,
                defaults={"wallpaper_id": Wallpaper.objects.get_default_wallpaper(), "wallpaper_type": "lashen"},
            )

            # 将用户添加的所有应用更新都桌面
            app_id_list = UserApp.objects.filter(user=user).values_list('id', flat=True)
            # app_id_list = [str(app_id) for app_id in app_id_list]
            user_setting.desk1 = ",".join(app_id_list)
            user_setting.save()
