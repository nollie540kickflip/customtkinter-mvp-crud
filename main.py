import customtkinter as ctk

from src.model.database import init_db
from src.model.user_model import UserModel
from src.presenter.main_presenter import MainPresenter
from src.view.main_view import MainView

# アプリケーションで使用するデータベースのファイルパス
DB_PATH = "app.db"


def main() -> None:
    """
    アプリケーションのメインエントリーポイント。
    テーマの設定、データベースの初期化、MVP各コンポーネントのセットアップを行い、
    アプリケーションを起動します。
    """
    # CustomTkinterの全体的な外観とカラーテーマを設定
    ctk.set_appearance_mode("System")  # モード: "System" (OSに依存), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # テーマ: "blue" (標準), "green", "dark-blue"

    # データベースとテーブルの初期化
    init_db(DB_PATH)

    # MVPアーキテクチャの各コンポーネントを初期化
    model = UserModel(DB_PATH)
    view = MainView()
    presenter = MainPresenter(model, view)

    # アプリケーションのメインループを開始
    presenter.run()


if __name__ == "__main__":
    main()
