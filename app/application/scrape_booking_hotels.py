class ScrapeBookingHotelsUseCase:

    def __init__(
        self,
        scraper,
        repository
    ):

        self.scraper = scraper

        self.repository = repository

    async def execute(self):

        hoteles = await self.scraper.scrape_hotels()

        await self.repository.save_many(
            hoteles
        )

        return hoteles