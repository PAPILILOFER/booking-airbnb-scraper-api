from abc import ABC, abstractmethod

class UserRepository(ABC):

    @abstractmethod
    async def create_user(
        self,
        email: str,
        password: str
    ):
        pass

    @abstractmethod
    async def get_by_email(
        self,
        email: str
    ):
        pass