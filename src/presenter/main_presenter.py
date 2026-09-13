import sqlite3

from src.model.user_model import UserModel
from src.view.main_view import MainView


class MainPresenter:
    """
    ModelとViewの仲介（Presenter）を行うクラス。
    UIのイベントを受け取り、Modelを使ってデータを処理し、Viewの表示を更新します。
    """

    def __init__(self, model: UserModel, view: MainView) -> None:
        """
        MainPresenterを初期化し、Viewのコールバックを設定します。

        Args:
            model (UserModel): ユーザー情報の操作を行うモデル
            view (MainView): UIの描画と入力受付を行うビュー
        """
        self.model = model
        self.view = view

        # Viewのコールバック関数にPresenterのメソッドをバインド
        self.view.on_add = self.handle_add
        self.view.on_update = self.handle_update
        self.view.on_delete = self.handle_delete
        self.view.on_clear = self.handle_clear

        # 初期データの読み込みと表示
        self.refresh_data()

    def refresh_data(self) -> None:
        """データベースから最新のユーザー一覧を取得し、Viewに表示させます。"""
        try:
            users = self.model.get_all()
            self.view.display_users(users)
        except sqlite3.Error as e:
            self.view.show_error(
                "データベースエラー", f"データの読み込みに失敗しました:\n{e}"
            )

    def handle_add(self) -> None:
        """追加ボタンが押された際の処理を行います。"""
        inputs = self.view.get_inputs()

        # 入力値のバリデーション
        if not inputs["name"] or not inputs["email"]:
            self.view.show_error("入力エラー", "名前とメールアドレスは必須です。")
            return

        if not self.view.ask_confirmation("確認", "新しいユーザーを追加しますか？"):
            return

        try:
            # 年齢が入力されていれば数値に変換、空ならNoneとして扱う
            age = int(inputs["age"]) if inputs["age"] else None
            self.model.create(inputs["name"], inputs["email"], age)
            self.view.clear_inputs()
            self.refresh_data()
        except ValueError:
            self.view.show_error("入力エラー", "年齢には有効な数値を入力してください。")
        except sqlite3.Error as e:
            self.view.show_error(
                "データベースエラー", f"ユーザーの追加に失敗しました:\n{e}"
            )

    def handle_update(self) -> None:
        """更新ボタンが押された際の処理を行います。"""
        inputs = self.view.get_inputs()
        user_id = inputs["id"]

        if user_id == 0:
            self.view.show_error(
                "選択エラー", "更新するユーザーをテーブルから選択してください。"
            )
            return

        # 入力値のバリデーション
        if not inputs["name"] or not inputs["email"]:
            self.view.show_error("入力エラー", "名前とメールアドレスは必須です。")
            return

        if not self.view.ask_confirmation("確認", "選択したユーザーの情報を更新しますか？"):
            return

        try:
            age = int(inputs["age"]) if inputs["age"] else None
            self.model.update(user_id, inputs["name"], inputs["email"], age)
            self.view.clear_inputs()
            self.refresh_data()
        except ValueError:
            self.view.show_error("入力エラー", "年齢には有効な数値を入力してください。")
        except sqlite3.Error as e:
            self.view.show_error(
                "データベースエラー", f"ユーザーの更新に失敗しました:\n{e}"
            )

    def handle_delete(self) -> None:
        """削除ボタンが押された際の処理を行います。"""
        inputs = self.view.get_inputs()
        user_id = inputs["id"]

        if user_id == 0:
            self.view.show_error(
                "選択エラー", "削除するユーザーをテーブルから選択してください。"
            )
            return

        if not self.view.ask_confirmation("確認", "本当に削除してよろしいですか？"):
            return

        try:
            self.model.delete(user_id)
            self.view.clear_inputs()
            self.refresh_data()
        except sqlite3.Error as e:
            self.view.show_error(
                "データベースエラー", f"ユーザーの削除に失敗しました:\n{e}"
            )

    def handle_clear(self) -> None:
        """クリアボタンが押された際、フォームの内容をリセットします。"""
        self.view.clear_inputs()

    def run(self) -> None:
        """アプリケーションのメインループを起動します。"""
        self.view.mainloop()
