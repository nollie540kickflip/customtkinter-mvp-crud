# customtkinter-mvp-crud

CustomTkinterとMVP (Model-View-Presenter) パターンを用いた、SQLiteテーブルのCRUD操作を行うサンプルアプリケーションです。

## 特徴
- **CustomTkinter**: モダンなダーク/ライトテーマ対応のGUI。
- **MVPアーキテクチャ**: ビジネスロジック（Model）、UI（View）、そしてそれらの橋渡し（Presenter）を分離し、保守性とテスト容易性を高めています。
- **SQLite3**: Python標準ライブラリの `sqlite3` を用いたローカルデータベース管理。

## ファイル構成
- `main.py`: アプリケーションのエントリーポイント。MVPコンポーネントを初期化します。
- `database.py`: データベース接続とテーブルの初期化。
- `user_model.py`: データベースのCRUD操作を担当するModel。
- `main_view.py`: CustomTkinterによるUI構築を担当するView。
- `main_presenter.py`: ModelとViewをつなぐPresenter。

## セットアップと実行

このプロジェクトはパッケージマネージャとして `uv` を使用しています。

1. **依存関係のインストール**:
   ```bash
   uv sync
   ```
   または
   ```bash
   uv add customtkinter
   ```

2. **アプリケーションの実行**:
   ```bash
   uv run python main.py
   ```

## 動作確認
アプリケーションを起動すると、データベース (`app.db`) が自動的に作成されます。
GUI上からユーザー情報の追加、更新、削除を行うことができます。

