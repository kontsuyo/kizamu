FROM python:3.13-slim

# 環境変数の設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="Asia/Tokyo"

# ユーザー・グループ情報
ARG USERNAME=user1
ARG GROUPNAME=user1
ARG UID=1000
ARG GID=1000

# 作業ディレクトリをユーザーのホーム配下に統一
WORKDIR /home/${USERNAME}/dev

# パッケージのインストール
RUN apt-get update -qq \
   && apt-get install -y --no-install-recommends \
   tzdata sudo \
   && rm -rf /var/lib/apt/lists/*

# Pythonモジュールのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 一般ユーザー作成
RUN groupadd -g ${GID} ${GROUPNAME} \
   && useradd -u ${UID} -g ${GID} -G sudo -m -s /bin/bash ${USERNAME} \
   && echo "%${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
   && chown -R ${USERNAME}:${GROUPNAME} /home/${USERNAME}

# 一般ユーザーに切替
USER ${USERNAME}
