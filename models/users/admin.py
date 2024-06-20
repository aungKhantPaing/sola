from models.users.user import User


class Admin(User):
    def display_info(self):
        return f"Administrator: {self.first_name} {self.last_name}"
