from abc import ABC, abstractmethod


class User(ABC):
    def __init__(
            self,
            first_name: str,
            last_name: str,
            username: str,
            password: str,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self._password = password  # _password is protected

    @abstractmethod
    def display_info(self):
        pass
