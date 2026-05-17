from abc import ABC
from abc import abstractmethod


class HotelScraperPort(ABC):

    @abstractmethod
    async def scrape_hotels(self):
        pass