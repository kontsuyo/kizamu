from datetime import timedelta

from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "change-me",
        "HOST": "db",  # compose.ymlで設定した名前
        "PORT": "5432",
    }
}
# 本番公開時は、特定のフロントエンドURLだけに絞りますが、
# 開発中はどこからでも繋がるようにしておくとスムーズです。
CORS_ALLOW_ALL_ORIGINS = True

# JWTの有効期限などの詳細設定（必要に応じて）
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ログディレクトリの作成
log_dir = BASE_DIR / "log"
log_dir.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_dir / "debug.log",
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 3,  # バックアップファイルの個数
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
