# -*- coding: utf-8 -*-
"""
从源环境数据库迁移轻应用(is_lapp=True)到当前环境。

迁移规则：
- external_url 中的域名替换为新域名
- logo 统一设为 /console/static/img/app_logo/default.png
- 其余字段保持源环境数据不变

源环境 DB 通过环境变量配置：
    MIGRATE_SOURCE_DB_HOST
    MIGRATE_SOURCE_DB_PORT
    MIGRATE_SOURCE_DB_NAME
    MIGRATE_SOURCE_DB_USER
    MIGRATE_SOURCE_DB_PASSWORD

用法：
    # 迁移（自动在写入前生成备份快照）
    python manage.py migrate_lapp migrate --new-domain paas.example.com [--dry-run]

    # 回退到指定备份
    python manage.py migrate_lapp rollback --backup-file lapp_backup_20260320_153000.json

    # 查看所有备份
    python manage.py migrate_lapp list-backups
"""
import json
import logging
import os
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from app.models import App

logger = logging.getLogger(__name__)

DEFAULT_LOGO = "/console/static/img/app_logo/default.png"
BACKUP_DIR_NAME = "lapp_migration_backups"

LAPP_QUERY = """
SELECT
    `name`, `code`, `introduction`, `name_en`, `introduction_en`,
    `creater`, `created_date`,
    `state`, `tags_id`, `is_already_test`, `is_already_online`,
    `first_test_time`, `first_online_time`,
    `language`, `is_use_celery`, `is_use_celery_beat`,
    `auth_token`, `deploy_token`, `is_saas`,
    `width`, `height`, `is_max`, `is_setbar`, `is_resize`,
    `use_count`, `is_default`, `is_display`, `open_mode`,
    `is_third`, `external_url`,
    `is_sysapp`, `is_platform`, `is_lapp`,
    `visiable_labels`, `star_num`,
    `from_paasv3`, `migrated_to_paasv3`,
    `app_tenant_mode`, `app_tenant_id`, `tenant_id`
FROM `paas_app`
WHERE `is_lapp` = 1
"""

FIELD_NAMES = [
    "name",
    "code",
    "introduction",
    "name_en",
    "introduction_en",
    "creater",
    "created_date",
    "state",
    "tags_id",
    "is_already_test",
    "is_already_online",
    "first_test_time",
    "first_online_time",
    "language",
    "is_use_celery",
    "is_use_celery_beat",
    "auth_token",
    "deploy_token",
    "is_saas",
    "width",
    "height",
    "is_max",
    "is_setbar",
    "is_resize",
    "use_count",
    "is_default",
    "is_display",
    "open_mode",
    "is_third",
    "external_url",
    "is_sysapp",
    "is_platform",
    "is_lapp",
    "visiable_labels",
    "star_num",
    "from_paasv3",
    "migrated_to_paasv3",
    "app_tenant_mode",
    "app_tenant_id",
    "tenant_id",
]


class BackupJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def get_backup_dir() -> Path:
    backup_dir = Path(os.environ.get("LAPP_BACKUP_DIR", BACKUP_DIR_NAME))
    backup_dir.mkdir(parents=True, exist_ok=True)
    return backup_dir


def replace_domain(url: str, new_domain: str) -> str:
    """将 URL 中的域名替换为 new_domain，保留路径、查询参数等。"""
    if not url:
        return url
    parsed = urlparse(url)
    replaced = parsed._replace(netloc=new_domain)
    return urlunparse(replaced)


def get_source_connection():
    """根据环境变量创建到源数据库的连接。"""
    required_vars = [
        "MIGRATE_SOURCE_DB_HOST",
        "MIGRATE_SOURCE_DB_NAME",
        "MIGRATE_SOURCE_DB_USER",
        "MIGRATE_SOURCE_DB_PASSWORD",
    ]
    missing = [v for v in required_vars if not os.environ.get(v)]
    if missing:
        raise CommandError(f"缺少源数据库环境变量: {', '.join(missing)}")

    return MySQLdb.connect(
        host=os.environ["MIGRATE_SOURCE_DB_HOST"],
        port=int(os.environ.get("MIGRATE_SOURCE_DB_PORT", 3306)),
        db=os.environ["MIGRATE_SOURCE_DB_NAME"],
        user=os.environ["MIGRATE_SOURCE_DB_USER"],
        passwd=os.environ["MIGRATE_SOURCE_DB_PASSWORD"],
        charset="utf8mb4",
    )


def snapshot_current_lapp_data(codes: list[str]) -> dict:
    """
    对当前环境中即将被影响的轻应用做快照。

    返回格式:
    {
        "timestamp": "...",
        "existing": { "code1": {字段...}, "code2": {字段...} },
        "new_codes": ["code3", "code4"]
    }
    existing: 迁移前已存在的记录（回退时恢复原值）
    new_codes: 迁移前不存在的 code（回退时删除）
    """
    from django.forms.models import model_to_dict

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "existing": {},
        "new_codes": [],
    }

    existing_apps = App._default_manager.filter(code__in=codes)
    existing_codes = set()

    for app in existing_apps:
        data = model_to_dict(app, exclude=["id", "developer"])
        data["logo"] = str(app.logo) if app.logo else ""
        data["tags_id"] = app.tags_id
        data.pop("tags", None)
        existing_codes.add(app.code)
        snapshot["existing"][app.code] = data

    snapshot["new_codes"] = [c for c in codes if c not in existing_codes]
    return snapshot


def save_backup(snapshot: dict) -> Path:
    backup_dir = get_backup_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = backup_dir / f"lapp_backup_{ts}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2, cls=BackupJSONEncoder)
    return filepath


class Command(BaseCommand):
    help = "轻应用迁移工具：migrate(迁移) / rollback(回退) / list-backups(查看备份)"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="action", help="子命令")

        migrate_parser = subparsers.add_parser("migrate", help="执行迁移")
        migrate_parser.add_argument(
            "--new-domain",
            required=True,
            help="新环境的域名，例如 apps.new-env.example.com",
        )
        migrate_parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="仅打印将要执行的操作，不实际写入数据库",
        )

        rollback_parser = subparsers.add_parser("rollback", help="回退迁移")
        rollback_parser.add_argument(
            "--backup-file",
            required=True,
            help="备份文件路径，如 lapp_backup_20260320_153000.json",
        )

        subparsers.add_parser("list-backups", help="列出所有备份文件")

    def handle(self, *args, **options):
        action = options.get("action")
        if not action:
            raise CommandError("请指定子命令: migrate / rollback / list-backups")

        handler = {
            "migrate": self._handle_migrate,
            "rollback": self._handle_rollback,
            "list-backups": self._handle_list_backups,
        }.get(action)

        if not handler:
            raise CommandError(f"未知子命令: {action}")
        handler(**options)

    # ── migrate ──────────────────────────────────────────────

    def _handle_migrate(self, **options):
        new_domain = options["new_domain"]
        dry_run = options["dry_run"]

        conn = get_source_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(LAPP_QUERY)
            rows = cursor.fetchall()
        finally:
            conn.close()

        if not rows:
            self.stdout.write(self.style.WARNING("源数据库中未找到轻应用(is_lapp=True)"))
            return

        self.stdout.write(f"从源数据库读取到 {len(rows)} 个轻应用")

        all_data = []
        for row in rows:
            data = dict(zip(FIELD_NAMES, row))
            data["external_url"] = replace_domain(data.get("external_url") or "", new_domain)
            all_data.append(data)

        if dry_run:
            for data in all_data:
                self.stdout.write(
                    f"  [DRY-RUN] code={data['code']}, " f"url: {data['external_url']}, " f"logo -> {DEFAULT_LOGO}"
                )
            self.stdout.write(self.style.WARNING(f"\n[DRY-RUN] 共 {len(all_data)} 个轻应用待迁移，未实际写入"))
            return

        codes = [d["code"] for d in all_data]
        snapshot = snapshot_current_lapp_data(codes)
        backup_path = save_backup(snapshot)
        self.stdout.write(self.style.SUCCESS(f"已生成备份: {backup_path}"))
        self.stdout.write(f"  其中已存在 {len(snapshot['existing'])} 条, " f"新增 {len(snapshot['new_codes'])} 条")

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with transaction.atomic():
            for data in all_data:
                code = data["code"]
                defaults = {k: v for k, v in data.items() if k != "code"}
                defaults["logo"] = DEFAULT_LOGO

                try:
                    _, created = App._default_manager.update_or_create(
                        code=code,
                        defaults=defaults,
                    )
                except Exception:
                    logger.exception("迁移轻应用 %s 失败", code)
                    skipped_count += 1
                    continue

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"  [新增] {code}: {data['external_url']}"))
                else:
                    updated_count += 1
                    self.stdout.write(f"  [更新] {code}: {data['external_url']}")

        self.stdout.write(
            self.style.SUCCESS(f"\n迁移完成: 新增 {created_count}, 更新 {updated_count}, 跳过 {skipped_count}")
        )
        self.stdout.write(f"如需回退，请执行: python manage.py migrate_lapp rollback --backup-file {backup_path}")

    # ── rollback ─────────────────────────────────────────────

    def _handle_rollback(self, **options):
        backup_file = options["backup_file"]

        filepath = Path(backup_file)
        if not filepath.is_absolute():
            filepath = get_backup_dir() / filepath
        if not filepath.exists():
            raise CommandError(f"备份文件不存在: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            snapshot = json.load(f)

        existing = snapshot.get("existing", {})
        new_codes = snapshot.get("new_codes", [])
        ts = snapshot.get("timestamp", "unknown")

        self.stdout.write(f"加载备份: {filepath} (创建于 {ts})")
        self.stdout.write(f"  将恢复 {len(existing)} 条已存在记录, 删除 {len(new_codes)} 条新增记录")

        confirm = input("确认回退? [y/N] ").strip().lower()
        if confirm != "y":
            self.stdout.write(self.style.WARNING("已取消回退"))
            return

        restored_count = 0
        deleted_count = 0
        error_count = 0

        with transaction.atomic():
            for code, data in existing.items():
                try:
                    data.pop("code", None)
                    data.pop("id", None)
                    data.pop("developer", None)
                    data.pop("tags", None)
                    App._default_manager.filter(code=code).update(**data)
                    restored_count += 1
                    self.stdout.write(f"  [恢复] {code}")
                except Exception:
                    logger.exception("恢复轻应用 %s 失败", code)
                    error_count += 1

            if new_codes:
                deleted, _ = App._default_manager.filter(code__in=new_codes).delete()
                deleted_count = deleted
                for code in new_codes:
                    self.stdout.write(f"  [删除] {code}")

        self.stdout.write(
            self.style.SUCCESS(f"\n回退完成: 恢复 {restored_count}, 删除 {deleted_count}, 失败 {error_count}")
        )

    # ── list-backups ─────────────────────────────────────────

    def _handle_list_backups(self, **options):
        backup_dir = get_backup_dir()
        files = sorted(backup_dir.glob("lapp_backup_*.json"), reverse=True)

        if not files:
            self.stdout.write(self.style.WARNING(f"暂无备份文件 (目录: {backup_dir})"))
            return

        self.stdout.write(f"备份目录: {backup_dir}\n")
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                ts = data.get("timestamp", "unknown")
                n_existing = len(data.get("existing", {}))
                n_new = len(data.get("new_codes", []))
                self.stdout.write(f"  {f.name}  (时间: {ts}, 已存在: {n_existing}, 新增: {n_new})")
            except Exception:
                self.stdout.write(f"  {f.name}  (无法解析)")
