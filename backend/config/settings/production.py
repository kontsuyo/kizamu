import os

import dj_database_url

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600
    )
}

# URLの信頼リスト
CSRF_TRUSTED_ORIGINS = [
    "https://aging-gallary.vercel.app",
    "https://backend-production-7724.up.railway.app",
]

# もし特定のURL（例：Reactの3000番ポート）だけに絞る場合はこちら
CORS_ALLOWED_ORIGINS = [
    "https://aging-gallary.vercel.app",
    "https://backend-production-7724.up.railway.app",
]

# cookieなど使う場合はTrue
CORS_ALLOW_CREDENTIALS = True

# 本番DBやセキュリティ設定
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True

# プロキシ（Railway）が渡してくるヘッダーを解釈する
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookieをセキュアにする（HTTPSのみで送信）
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",  # 本番はINFO以上でOK
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "my-app-auth",
    "JWT_AUTH_REFRESH_COOKIE": "my-refresh-token",
    "JWT_AUTH_HTTPONLY": True,  # JSからトークンを盗まれないようにTrue
    "JWT_AUTH_SECURE": True,  # HTTPS経由のみに限定
    "JWT_AUTH_SAMESITE": "Lax",  # VercelとRailwayのドメインが違うので 'Lax' または 'None'
}
