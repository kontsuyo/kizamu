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

# ここで一度、インストールされたパッケージを確認するログを出す（デバッグ用）
RUN pip list

COPY . .

RUN DJANGO_SETTINGS_MODULE=config.settings.production
# collectstatic の実行
# RUN python manage.py collectstatic --noinput
# RUN SECRET_KEY=dummy DEBUG=False python manage.py collectstatic --noinput

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:${PORT} config.wsgi:application"]
