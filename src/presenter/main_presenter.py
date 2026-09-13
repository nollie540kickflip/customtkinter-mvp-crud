from src.model.user_model import UserModel
from src.view.main_view import MainView


class MainPresenter:
    def __init__(self, model: UserModel, view: MainView) -> None:
        self.model = model
        self.view = view

        # Bind view callbacks to presenter methods
        self.view.on_add = self.handle_add
        self.view.on_update = self.handle_update
        self.view.on_delete = self.handle_delete
        self.view.on_clear = self.handle_clear

        # Load initial data
        self.refresh_data()

    def refresh_data(self) -> None:
        try:
            users = self.model.get_all()
            self.view.display_users(users)
        except Exception as e:
            self.view.show_error("Database Error", f"Failed to load data:\n{e}")

    def handle_add(self) -> None:
        inputs = self.view.get_inputs()

        # Validation
        if not inputs["name"] or not inputs["email"]:
            self.view.show_error("Validation Error", "Name and Email are required.")
            return

        try:
            age = int(inputs["age"]) if inputs["age"] else None
            self.model.create(inputs["name"], inputs["email"], age)
            self.view.clear_inputs()
            self.refresh_data()
        except ValueError:
            self.view.show_error("Validation Error", "Age must be a valid number.")
        except Exception as e:
            self.view.show_error("Database Error", f"Failed to add user:\n{e}")

    def handle_update(self) -> None:
        inputs = self.view.get_inputs()
        user_id = inputs["id"]

        if user_id == 0:
            self.view.show_error("Selection Error", "Please select a user to update.")
            return

        if not inputs["name"] or not inputs["email"]:
            self.view.show_error("Validation Error", "Name and Email are required.")
            return

        try:
            age = int(inputs["age"]) if inputs["age"] else None
            self.model.update(user_id, inputs["name"], inputs["email"], age)
            self.view.clear_inputs()
            self.refresh_data()
        except ValueError:
            self.view.show_error("Validation Error", "Age must be a valid number.")
        except Exception as e:
            self.view.show_error("Database Error", f"Failed to update user:\n{e}")

    def handle_delete(self) -> None:
        inputs = self.view.get_inputs()
        user_id = inputs["id"]

        if user_id == 0:
            self.view.show_error("Selection Error", "Please select a user to delete.")
            return

        try:
            self.model.delete(user_id)
            self.view.clear_inputs()
            self.refresh_data()
        except Exception as e:
            self.view.show_error("Database Error", f"Failed to delete user:\n{e}")

    def handle_clear(self) -> None:
        self.view.clear_inputs()

    def run(self) -> None:
        self.view.mainloop()
