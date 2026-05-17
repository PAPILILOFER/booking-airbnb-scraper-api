from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import (
    get_mongo_db
)


from app.infrastructure.scrapers.Playwright_airbnb_attraction_scraper import (
    PlaywrightAirbnbAttractionScraper
)

from app.infrastructure.scrapers.playwright_booking_scraper import (
    PlaywrightBookingScraper
)

from app.domain.repositories.mongo_hotel_repository import (
    MongoHotelRepository
)

from app.application.scrape_booking_hotels import (
    ScrapeBookingHotelsUseCase
)

from app.infrastructure.scrapers.playwright_booking_attractions_scraper import (
    PlaywrightBookingAttractionsScraper
)

from app.domain.repositories.mongo_attraction_repository import (
    MongoAttractionRepository
)

from app.application.scrape_booking_attractions import (
    ScrapeBookingAttractionsUseCase
)

from app.infrastructure.scrapers.playwright_airbnb_scraper import (
    PlaywrightAirbnbScraper
)

from app.domain.repositories.mongo_airbnb_hotel_repository import (
    MongoAirbnbRepository
)

from app.application.scrape_airbnb_hotels import (
    ScrapeAirbnbHotelsUseCase
)

from app.application.scrape_airbnb_attraction import (
    ScrapeAirbnbAttractionsUseCase
    )

from app.domain.repositories.mongo_airbnb_attraction_repository import (
    MongoAirbnbAttractionRepository
)
router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"]
)


@router.post("/booking/hotels")
async def scrape_booking_hotels(
    mongo_db = Depends(get_mongo_db)
):

    scraper = PlaywrightBookingScraper()

    repository = MongoHotelRepository(
        mongo_db
    )

    use_case = ScrapeBookingHotelsUseCase(
        scraper=scraper,
        repository=repository
    )

    hoteles = await use_case.execute()

    return {
        "message": "Scraping completado",
        "count": len(hoteles),
        "results": hoteles
    }


@router.get("/booking/hotels")
async def get_hotels(
    mongo_db = Depends(get_mongo_db)
):

    repository = MongoHotelRepository(
        mongo_db
    )

    hoteles = await repository.get_all()

    return {
        "count": len(hoteles),
        "results": hoteles
    }
    
@router.post("/booking/attractions")
async def scrape_booking_attractions(
    mongo_db = Depends(get_mongo_db)
):

    scraper = (
        PlaywrightBookingAttractionsScraper()
    )

    repository = (
        MongoAttractionRepository(
            mongo_db
        )
    )

    use_case = (
        ScrapeBookingAttractionsUseCase(
            scraper=scraper,
            repository=repository
        )
    )

    attractions = await use_case.execute()

    return {
        "message": "Scraping completado",
        "count": len(attractions),
        "results": attractions
    }


@router.get("/booking/attractions")
async def get_attractions(
    mongo_db = Depends(get_mongo_db)
):

    repository = (
        MongoAttractionRepository(
            mongo_db
        )
    )

    attractions = await repository.get_all()

    return {
        "count": len(attractions),
        "results": attractions
    }
    
@router.post("/airbnb/hotels")
async def scrape_airbnb_hotels(
    mongo_db = Depends(get_mongo_db)
):

    scraper = PlaywrightAirbnbScraper()

    repository = MongoAirbnbRepository(
        mongo_db
    )

    use_case = ScrapeAirbnbHotelsUseCase(
        scraper=scraper,
        repository=repository
    )

    hoteles = await use_case.execute()

    return {
        "message": "Scraping Airbnb completado",
        "count": len(hoteles),
        "results": hoteles
    }
    
@router.get("/airbnb/hotels")
async def get_airbnb_hotels(
    mongo_db = Depends(get_mongo_db)
):

    repository = MongoAirbnbRepository(
        mongo_db
    )

    hoteles = await repository.get_all()

    return {
        "count": len(hoteles),
        "results": hoteles
    }
    
@router.post("/airbnb/attractions")
async def scrape_airbnb_attractions(
    mongo_db = Depends(get_mongo_db)
):

    scraper = (
        PlaywrightAirbnbAttractionScraper()
    )

    repository = (
        MongoAirbnbAttractionRepository(
            mongo_db
        )
    )

    use_case = (
        ScrapeAirbnbAttractionsUseCase(
            scraper=scraper,
            repository=repository
        )
    )

    attractions = await use_case.execute()

    return {
        "count": len(attractions),
        "results": attractions
    }


@router.get("/airbnb/attractions")
async def get_airbnb_attractions(
    mongo_db = Depends(get_mongo_db)
):

    repository = (
        MongoAirbnbAttractionRepository(
            mongo_db
        )
    )

    attractions  = await repository.get_all()

    return {
        "count": len(attractions),
        "results": attractions
    }