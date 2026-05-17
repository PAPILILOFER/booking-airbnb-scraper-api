import random

from playwright.async_api import (
    async_playwright
)

from app.domain.ports.hotel_scraper_port import (
    HotelScraperPort
)


class PlaywrightBookingScraper(
    HotelScraperPort
):

    async def scrape_hotels(self):

        url = (
            "https://www.booking.com/"
            "searchresults.es.html"
            "?dest_id=47&dest_type=country"
        )

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = await browser.new_context(
                viewport={
                    "width": 1920,
                    "height": 1080
                },
                locale="es-ES",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )

            page = await context.new_page()

            try:

                await page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                await page.wait_for_timeout(5000)

                for _ in range(5):

                    await page.evaluate(
                        "window.scrollBy(0, 1000)"
                    )

                    await page.wait_for_timeout(
                        random.randint(1000, 2000)
                    )

                try:

                    await page.click(
                        'button[aria-label="Cerrar"]',
                        timeout=2000
                    )

                except:
                    pass

                hoteles = await page.evaluate("""() => {

                        return Array.from(
                            document.querySelectorAll('[data-testid="property-card"]')
                        ).map(card => {

                            const title =
                                card.querySelector('[data-testid="title"]')
                                ?.textContent
                                ?.trim() || null;

                            const location =
                                card.querySelector('[data-testid="address-link"]')
                                ?.textContent
                                ?.trim() || null;
                                                                                        
                            const image =
                                card.querySelector('img')
                                ?.src || null;

                            const link =
                                card.querySelector('[data-testid="title-link"]')
                                ?.href ||
                                card.querySelector('a')
                                ?.href || null;

                            const reviewContainer =
                                card.querySelector('[data-testid="review-score"]');

                            const scoreText =
                                reviewContainer
                                ?.querySelector('[aria-hidden="true"]')
                                ?.textContent
                                ?.trim() || null;

                            const score =
                                scoreText
                                ? scoreText.replace(',', '.')
                                : null;

                            const rating  =
                                reviewContainer
                                ?.querySelector('.becbee2f63')
                                ?.textContent
                                ?.trim() || null;

                            const commentsText  =
                                reviewContainer
                                ?.querySelector('.eaa8455879')
                                ?.textContent
                                ?.trim() || null;

                            const numComments =
                                commentsText
                                ?.match(/[0-9,.]+/)
                                ?.[0]
                                ?.replace(',', '') || null;
                                
                           return {
                            title,
                            location,                        
                            image,
                            score,
                            rating,
                            numComments,
                            link,
                            source: 'booking'
                            };
                        });
                    }""")

                hoteles_filtrados = [
                    hotel
                    for hotel in hoteles
                    if hotel.get("title")
                ]

                return hoteles_filtrados

            finally:

                await browser.close()