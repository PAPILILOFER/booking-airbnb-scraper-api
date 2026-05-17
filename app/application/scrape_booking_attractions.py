class ScrapeBookingAttractionsUseCase:

    def __init__(
        self,
        scraper,
        repository
    ):

        self.scraper = scraper

        self.repository = repository

    async def execute(self):

        attractions = await self.scraper.scrape_attractions()

        await self.repository.save_many(
            attractions
        )

        return attractions