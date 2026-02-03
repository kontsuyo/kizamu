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

# Vercelのドメインを許可リストに追加
CORS_ALLOWED_ORIGINS = [
    "https://aging-gallary.vercel.app",  # Vercelで発行されたURL
]

# DjangoのCSRF対策でもVercelを信用する
CSRF_TRUSTED_ORIGINS = [
    "https://aging-gallary.vercel.app",
]

# cookieなど使う場合はTrue
CORS_ALLOW_CREDENTIALS = True

# 本番DBやセキュリティ設定
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
