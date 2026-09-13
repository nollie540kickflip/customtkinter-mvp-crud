import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MVP CRUD Sample")
        self.geometry("700x500")

        # Callbacks that will be set by the Presenter
        self.on_add = None
        self.on_update = None
        self.on_delete = None
        self.on_clear = None

        self._setup_ui()

    def _setup_ui(self):
        # Configure layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Left Frame (Form) ---
        self.form_frame = ctk.CTkFrame(self, width=250)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.form_frame.grid_propagate(False)

        ctk.CTkLabel(
            self.form_frame,
            text="User Details",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(pady=(10, 20))

        # ID (Hidden from user, but we store it in a variable)
        self.selected_user_id = tk.IntVar(value=0)

        # Name
        ctk.CTkLabel(self.form_frame, text="Name:").pack(anchor="w", padx=10)
        self.name_entry = ctk.CTkEntry(self.form_frame)
        self.name_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Email
        ctk.CTkLabel(self.form_frame, text="Email:").pack(anchor="w", padx=10)
        self.email_entry = ctk.CTkEntry(self.form_frame)
        self.email_entry.pack(fill="x", padx=10, pady=(0, 10))

        # Age
        ctk.CTkLabel(self.form_frame, text="Age:").pack(anchor="w", padx=10)
        self.age_entry = ctk.CTkEntry(self.form_frame)
        self.age_entry.pack(fill="x", padx=10, pady=(0, 20))

        # Buttons
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

        # --- Right Frame (Data Table) ---
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        # Style the Treeview to match CustomTkinter somewhat
        style = ttk.Style(self)
        style.theme_use("default")

        # Configure colors based on appearance mode
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

        # Treeview
        columns = ("id", "name", "email", "age")
        self.tree = ttk.Treeview(
            self.table_frame, columns=columns, show="headings", style="Treeview"
        )

        # Define headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("age", text="Age")

        # Define columns
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("email", width=200, anchor="w")
        self.tree.column("age", width=50, anchor="center")

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(self.table_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y", padx=5, pady=5)
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Bind select event
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        values = item["values"]

        # Populate form
        self.selected_user_id.set(values[0])
        self.set_name(values[1])
        self.set_email(values[2])
        self.set_age(values[3])

    # --- Methods for Presenter ---

    def get_inputs(self):
        return {
            "id": self.selected_user_id.get(),
            "name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip(),
            "age": self.age_entry.get().strip(),
        }

    def set_name(self, value):
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, str(value))

    def set_email(self, value):
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, str(value))

    def set_age(self, value):
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, str(value))

    def clear_inputs(self):
        self.selected_user_id.set(0)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        # Deselect treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def display_users(self, users):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new items
        for user in users:
            self.tree.insert("", tk.END, values=user)

    def show_error(self, title, message):
        # In a real app, use CTkMessagebox or similar.
        # For simplicity, we just print to console or create a simple toplevel.
        # Using a simple tkinter messagebox for ease.
        from tkinter import messagebox

        messagebox.showerror(title, message)

    def show_info(self, title, message):
        from tkinter import messagebox

        messagebox.showinfo(title, message)
