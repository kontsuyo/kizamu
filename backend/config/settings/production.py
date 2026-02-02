from .base import *

import dj_database_url
import os

DEBUG = False
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"), conn_max_age=600
    )
}
# 本番DBやセキュリティ設定
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
