from abc import ABC
from abc import abstractmethod


class AttractionScraperPort(ABC):

    @abstractmethod
    async def scrape_attractions(self):
        pass