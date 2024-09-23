from abc import ABC, abstractmethod

from models.user import UserBase


class DbInterface(ABC):
    @abstractmethod
    async def user_exists(self, user: UserBase) -> (int, Exception):
        pass

    @abstractmethod
    async def register_user(self, user: UserBase) -> (int, Exception):
        pass

    @abstractmethod
    async def user_login(self, user: UserBase) -> (int, Exception):
        pass
