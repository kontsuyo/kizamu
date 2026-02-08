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

# もし特定のURL（例：Reactの3000番ポート）だけに絞る場合はこちら
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

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
