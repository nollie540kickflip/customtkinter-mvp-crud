import customtkinter as ctk

from src.model.database import init_db
from src.model.user_model import UserModel
from src.presenter.main_presenter import MainPresenter
from src.view.main_view import MainView

DB_PATH = "app.db"


def main() -> None:
    # Set global appearance mode and color theme
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme(
        "blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"

    # Initialize the database and table
    init_db(DB_PATH)

    # Initialize MVP components
    model = UserModel(DB_PATH)
    view = MainView()
    presenter = MainPresenter(model, view)

    # Start the application
    presenter.run()


if __name__ == "__main__":
    main()
