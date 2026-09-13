import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class MainView(ctk.CTk):
    """
    アプリケーションのメイン画面を構築するクラス（View）。
    ロジックは持たず、ユーザー入力の受け付けと画面の描画のみを担当します。
    """

    def __init__(self):
        """MainViewを初期化し、UI要素を配置します。"""
        super().__init__()

        self.title("MVP CRUD Sample")
        self.geometry("700x500")

        # Presenter側でセットされるコールバック関数の初期化
        self.on_add = None
        self.on_update = None
        self.on_delete = None
        self.on_clear = None

        self._setup_ui()

    def _setup_ui(self):
        """UIのレイアウトとウィジェットの構成を行います。"""
        # 全体のレイアウト設定
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 左側フレーム（入力フォーム） ---
        self.form_frame = ctk.CTkFrame(self, width=250)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.form_frame.grid_propagate(False)

        ctk.CTkLabel(
            self.form_frame,
            text="User Details",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=(10, 20))

        # ID（ユーザーには非表示ですが、更新・削除用に変数として保持します）
        self.selected_user_id = tk.IntVar(value=0)

        # Name（名前）入力フィールド
        ctk.CTkLabel(self.form_frame, text="Name:").pack(anchor="w", padx=10)
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Email（メールアドレス）入力フィールド
        ctk.CTkLabel(self.form_frame, text="Email:").pack(anchor="w", padx=10)
        self.email_entry = ctk.CTkEntry(self.form_frame)
        self.email_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Age（年齢）入力フィールド
        ctk.CTkLabel(self.form_frame, text="Age:").pack(anchor="w", padx=10)
        self.age_entry = ctk.CTkEntry(self.form_frame)
        self.age_entry.pack(fill="x", padx=10, pady=(0, 20))

        # 各種操作ボタン
        self.btn_add = ctk.CTkButton(
            self.form_frame,
            text="Add",
            command=lambda: self.on_add() if self.on_add else None,
        )
        self.btn_add.pack(fill="x", padx=10, pady=5)

        self.btn_update = ctk.CTkButton(
            self.form_frame,
            text="Update",
            command=lambda: self.on_update() if self.on_update else None,
        )
        self.btn_update.pack(fill="x", padx=10, pady=5)

        self.btn_delete = ctk.CTkButton(
            self.form_frame,
            text="Delete",
            fg_color="darkred",
            hover_color="red",
            command=lambda: self.on_delete() if self.on_delete else None,
        )
        self.btn_delete.pack(fill="x", padx=10, pady=5)

        self.btn_clear = ctk.CTkButton(
            self.form_frame,
            text="Clear Form",
            fg_color="gray",
            command=lambda: self.on_clear() if self.on_clear else None,
        )
        self.btn_clear.pack(fill="x", padx=10, pady=20)

        # --- 右側フレーム（データテーブル表示） ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # CustomTkinterのテーマに合わせて標準のTreeviewのスタイルを調整
        style = ttk.Style(self)
        style.theme_use("default")

        # 現在のアピアランスモード（Dark/Light）に基づいて色を取得
        bg_color = self._apply_appearance_mode(
            ctk.ThemeManager.theme["CTkFrame"]["fg_color"]
        )
        text_color = self._apply_appearance_mode(
            ctk.ThemeManager.theme["CTkLabel"]["text_color"]
        )
        selected_color = self._apply_appearance_mode(
            ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        )

        style.configure(
            "Treeview",
            background=bg_color,
            foreground=text_color,
            rowheight=25,
            fieldbackground=bg_color,
            bordercolor=bg_color,
            borderwidth=0,
        )
        style.map("Treeview", background=[("selected", selected_color)])
        style.configure(
            "Treeview.Heading",
            background=bg_color,
            foreground=text_color,
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", bg_color)])

        # Treeview（テーブル）の設定
        columns = ("id", "name", "email", "age")
        self.tree = ttk.Treeview(
            self.table_frame, columns=columns, show="headings", style="Treeview"
        )

        # カラム見出しの設定時にソートコマンドをバインド
        for col in columns:
            self.tree.heading(
                col,
                text=col.capitalize() if col != "id" else "ID",
                command=lambda c=col: self._sort_by_column(c, False),
            )

        # カラム幅と配置の設定
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("age", width=50, anchor="center")

        # スクロールバーの設定
        scrollbar = ctk.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y", padx=5, pady=5)
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 行を選択した際のイベントバインディング
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        """
        テーブルの行が選択された際に、選択されたデータをフォームに反映します。
        """
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        values = item["values"]

        # フォームに値をセット
        self.selected_user_id.set(values[0])
        self.set_name(values[1])
        self.set_email(values[2])
        self.set_age(values[3])

    def _sort_by_column(self, col: str, reverse: bool):
        """指定された列でテーブルのデータをソートします。"""
        # 現在表示されている全データを取得
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # IDや年齢など数値の列は数値として比較する
        if col in ("id", "age"):
            items.sort(
                key=lambda t: int(t[0]) if t[0] and str(t[0]).isdigit() else 0,
                reverse=reverse,
            )
        else:
            items.sort(reverse=reverse)

        # ソート結果に従ってアイテムを並び替え
        for index, (_, k) in enumerate(items):
            self.tree.move(k, "", index)

        # 次回クリック時は昇順/降順を逆にするようにコマンドを更新
        self.tree.heading(col, command=lambda: self._sort_by_column(col, not reverse))

    # --- Presenterから呼び出されるメソッド群 ---

    def get_inputs(self) -> dict:
        """
        現在フォームに入力されている値を取得します。

        Returns:
            dict: 入力値の辞書 (id, name, email, age)
        """
        return {
            "id": self.selected_user_id.get(),
            "name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "age": self.age_entry.get().strip(),
        }

    def set_name(self, value: str):
        """名前入力フィールドに値をセットします。"""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, str(value))

    def set_email(self, value: str):
        """メールアドレス入力フィールドに値をセットします。"""
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, str(value))

    def set_age(self, value: str):
        """年齢入力フィールドに値をセットします。"""
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, str(value))

    def clear_inputs(self):
        """すべての入力フィールドをクリアし、テーブルの選択状態を解除します。"""
        self.selected_user_id.set(0)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        # テーブルの選択を解除
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def display_users(self, users: list[tuple]):
        """
        テーブルにユーザー情報を表示します。
        既存の表示データはすべてクリアされます。

        Args:
            users (list[tuple]): 表示するユーザーデータのリスト
        """
        # 既存のアイテムをクリア
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 新しいアイテムを追加
        for user in users:
            self.tree.insert("", tk.END, values=user)

    def show_error(self, title: str, message: str):
        """
        エラーメッセージダイアログを表示します。

        Args:
            title (str): ダイアログのタイトル
            message (str): 表示するエラーメッセージ
        """
        # 実際のアプリではCTkMessagebox等の利用が推奨されますが、
        # ここでは簡易的にtkinter標準のメッセージボックスを使用します
        from tkinter import messagebox

        messagebox.showerror(title, message)

    def show_info(self, title: str, message: str):
        """
        情報メッセージダイアログを表示します。

        Args:
            title (str): ダイアログのタイトル
            message (str): 表示するメッセージ
        """
        from tkinter import messagebox

        messagebox.showinfo(title, message)

    def ask_confirmation(self, title: str, message: str) -> bool:
        """
        確認ダイアログを表示します。

        Args:
            title (str): ダイアログのタイトル
            message (str): 表示する確認メッセージ

        Returns:
            bool: ユーザーが「はい」を選択した場合は True、「いいえ」の場合は False
        """
        from tkinter import messagebox

        return messagebox.askyesno(title, message)
