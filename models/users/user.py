from abc import ABC, abstractmethod


class User(ABC):
    def __init__(
            self,
            username: str,
            password: str,
            first_name: str,
            last_name: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self._password = password  # _password is protected

    def verify_password(self, password):
        return self._password == password

    @abstractmethod
    def display_info(self):
        pass
