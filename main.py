import customtkinter as ctk

from database import init_db
from main_presenter import MainPresenter
from main_view import MainView
from user_model import UserModel


def main():
    # Set global appearance mode and color theme
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    # Initialize the database and table
    init_db()

    # Initialize MVP components
    model = UserModel()
    view = MainView()
    presenter = MainPresenter(model, view)

    # Start the application
    presenter.run()


if __name__ == "__main__":
    main()
