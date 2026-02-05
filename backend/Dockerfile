# backend/Dockerfile

FROM python:3.13-slim

# システムの依存関係（念のため）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先に pip 自体をアップグレード
RUN pip install --upgrade pip

# requirements.txt を確実にコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ビルド時のみ必要なダミー値を環境変数として設定
ENV DJANGO_SETTINGS_MODULE=config.settings.production
ENV SECRET_KEY=dummy-key-for-build-only
ENV DEBUG=False

# Cloudinaryなどの外部サービス用ダミー変数
ENV CLOUD_NAME=dummy
ENV API_KEY=dummy
ENV API_SECRET=dummy

# インストールされているコマンド一覧に collectstatic があるか確認
RUN python manage.py help

# collectstatic の実行
RUN python manage.py collectstatic --noinput

# ここも 8080 に固定してしまう
CMD python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8080 config.wsgi:application

# 起動時に「adminがいなければ作る」という処理を1行でねじ込む
# CMD python manage.py migrate && \
#     python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'testpass123')" && \
#     gunicorn --bind 0.0.0.0:8080 config.wsgi:application
