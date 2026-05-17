from abc import ABC
from abc import abstractmethod


class AirbnbAttractionScraperPort(ABC):

    @abstractmethod
    async def scrape_attractions(self):
        pass