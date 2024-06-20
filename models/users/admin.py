from user import User


class Administrator(User):
    def display_info(self):
        return f"Administrator: {self.first_name} {self.last_name}"
