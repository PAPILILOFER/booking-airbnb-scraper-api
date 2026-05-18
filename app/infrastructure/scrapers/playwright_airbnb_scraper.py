import random
import os
from dotenv import load_dotenv

load_dotenv()
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

from playwright.async_api import (
    async_playwright
)

from app.domain.ports.airbnb_scraper_port import (
    AirbnbScraperPort
)


class PlaywrightAirbnbScraper(
        AirbnbScraperPort
):

    async def scrape_hotels(self):

        url = (
            "https://www.airbnb.com.co/"
            "s/Colombia/homes"
        )

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=HEADLESS,
                args=[
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = await browser.new_context(
                viewport={
                    "width": 1920,
                    "height": 1080
                },
                locale="es-CO",
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

                for _ in range(8):

                    await page.evaluate(
                        "window.scrollBy(0, 1200)"
                    )

                    await page.wait_for_timeout(
                        random.randint(1500, 2500)
                    )

                propiedades = await page.evaluate("""() => {

               const resultados = [];

                    const listings = document.querySelectorAll(
                        'a[rel="noopener noreferrer nofollow"][target^="listing_"]'
                    );

                    listings.forEach(listing => {

                        try {

                            const container =
                                listing.closest(
                                    '[data-testid="card-container"]'
                                );

                            if (!container) return;

                            const title =
                                container.querySelector(
                                    '[data-testid="listing-card-title"]'
                                )
                                ?.textContent
                                ?.trim() || null;

                            const image =
                                container.querySelector('img')
                                ?.src || null;

                            const link =
                                listing.href || null;

                            const location =
                                container.querySelector(
                                    '[data-testid="listing-card-subtitle"]'
                                )
                                ?.textContent
                                ?.trim() || null;

                            const propertyType =
                                container.querySelector(
                                    '[data-testid="listing-card-subtitle"]'
                                )
                                ?.textContent
                                ?.trim() || null;

                            let price = null;
                            let numericPrice = null;

                            const fullPriceText =
                                    container.innerText
                                    .replace(/\s+/g, ' ')
                                    .trim();

                                const priceMatch =
                                    fullPriceText.match(
                                        /\$[0-9.,]+\s*COP\s*por\s*[0-9]+\s*noches/i
                                    );

                                if (priceMatch) {

                                    price =
                                        priceMatch[0]
                                        .replace(/\s+/g, ' ')
                                        .trim();

                                    const numericMatch =
                                        price.match(/\$([0-9.,]+)/);

                                    if (numericMatch) {

                                        numericPrice =
                                            numericMatch[1]
                                            .replace(/\./g, '')
                                            .replace(',', '');
                                        }
                                    }
                               
                            let score = null;
                            let numComments = null;

                            const fullText =
                                container.innerText || '';

                            const scoreMatch =
                                fullText.match(
                                    /([0-9]+[.,][0-9]+)\\s*\\(([0-9]+)\\)/
                                );

                            if (scoreMatch) {

                                score =
                                    scoreMatch[1]
                                    .replace(',', '.');

                                numComments =
                                    scoreMatch[2];
                            }

                            resultados.push({

                                title,

                                location,

                                image,

                                score,

                                numComments,

                                propertyType,

                                price,

                                numericPrice,

                                link,

                                source: 'airbnb'
                            });

                        } catch (error) {
                            console.log(error);
                        }
                    });

                    return resultados;
                }""")

                propiedades_filtradas = [
                    propiedad
                    for propiedad in propiedades
                    if propiedad.get("title")
                ]

                return propiedades_filtradas

            finally:

                await browser.close()