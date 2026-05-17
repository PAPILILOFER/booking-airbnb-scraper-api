from abc import ABC
from abc import abstractmethod


class AirbnbAttractionRepository(ABC):

    @abstractmethod
    async def save_many(
        self,
        attractions: list
    ):
        pass

    @abstractmethod
    async def get_all(self):
        pass