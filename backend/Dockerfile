# backend/Dockerfile

FROM python:3.13-slim

WORKDIR /app

# backend/requirements.txt をコピー
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# backend フォルダ内をすべてコピー
COPY . .

RUN python manage.py collectstatic --noinput

# 起動コマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "config.wsgi:application"]
