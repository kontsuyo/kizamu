# プロジェクト概要: Aging Gallery - KIZAMU
海外アプリ「Patina Project」の日本版を目指した、ブーツのエイジング記録・共有アプリ。将来的には服やアクセサリーなど他の製品にも対応予定。

## アプリの目的
- ユーザーが所有するブーツの着用回数やケア（オイルアップ、ソール交換等）を記録する。
- 経過日数や着用頻度に応じた革の変化（エイジング）を写真で時系列に管理する。

## 技術スタック
- **Backend:** Django Rest Framework (Python)
- **Frontend:** Next.js
- **Database:** PostgreSQL

## コーディング方針
- **General:** - 変数名や関数名は英語を使用するが、コメントやドキュメントは日本語で記載する。
  - シンプルでメンテナンスしやすいコードを優先する。
- **Backend (DRY):** - ModelSerializerを基本とし、APIはRESTfulな設計にする。
  - 認証はJWTを使用する予定。
- **Frontend (Next.js):** - 関数コンポーネントとHooks（useState, useEffect）を使用する。
  - スタイリングはStyleSheetまたはStyled-componentsを使用する。

## 現在のフェーズ
- 開発初期段階。
<!-- - まずは「ブーツ登録機能」と「写真投稿機能」のMVP（最小機能）開発を目指している。 -->
- バックエンドのMVP開発はMVP開発は終了。
- これからフロントエンド開発に入る。
