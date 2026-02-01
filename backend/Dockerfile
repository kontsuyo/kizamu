# backend/Dockerfile

FROM python:3.13-slim

WORKDIR /app

# backend/requirements.txt をコピー
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# backend フォルダ内をすべてコピー
COPY . .

# collectstatic を実行するときだけ、ダミーの環境変数を注入する
# これで settings.py の読み込みエラーを回避します
RUN DJANGO_SETTINGS_MODULE=config.settings \
    SECRET_KEY=build-dummy \
    DEBUG=False \
    ALLOWED_HOSTS=* \
    python manage.py collectstatic --noinput

# 起動コマンド（ここではRailwayのVariablesが本物の値として注入されます）
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "config.wsgi:application"]

# RUN python manage.py collectstatic --noinput

# # 起動コマンド
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]
