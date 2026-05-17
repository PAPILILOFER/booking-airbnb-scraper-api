from abc import ABC
from abc import abstractmethod


class AirbnbRepositoryPort(ABC):

    @abstractmethod
    async def save_many(
        self,
        hotels: list
    ):
        pass

    @abstractmethod
    async def get_all(self):
        pass