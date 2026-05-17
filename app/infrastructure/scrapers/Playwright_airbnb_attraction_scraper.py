import random

from playwright.async_api import (
    async_playwright
)

from app.domain.ports.airbnb_attraction_scraper_port import (
    AirbnbAttractionScraperPort
)


class PlaywrightAirbnbAttractionScraper(
    AirbnbAttractionScraperPort
):

    async def scrape_attractions(self):

        url = (
            "https://www.airbnb.com.co/"
            "s/Colombia/experiences"
            "?place_id=ChIJo5QVrjqkFY4RQKPy7wSaDZo"
            "&refinement_paths%5B%5D=%2Fexperiences"
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

                for _ in range(10):

                    await page.evaluate(
                        "window.scrollBy(0, 1000)"
                    )

                    await page.wait_for_timeout(
                        random.randint(1500, 2500)
                    )

                attractions = await page.evaluate("""() => {

                    const resultados = [];
                    const ids = new Set();

                    const cards = document.querySelectorAll('a[href*="/experiences/"]');

                    cards.forEach(linkElement => {

                        try {

                            const link = linkElement.href;

                            if (ids.has(link)) return;

                            ids.add(link);

                            const container =
                                linkElement.closest('div');

                            if (!container) return;

                            const fullText =
                                container.innerText
                                .replace(/\\s+/g, ' ')
                                .trim();

                            const title =
                                container.querySelector('div[data-testid="listing-card-title"]')
                                ?.textContent
                                ?.trim() || null;

                            const image =
                                container.querySelector('img')
                                ?.src || null;

                            let price = null;
                            let numericPrice = null;

                            const priceMatch =
                                fullText.match(
                                    /\\$[0-9.,]+/
                                );

                            if (priceMatch) {

                                price = priceMatch[0];

                                numericPrice =
                                    price
                                    .replace('$', '')
                                    .replace(/\\./g, '')
                                    .replace(/,/g, '');
                            }

                            let score = null;
                            const match1 = fullText.match(/([0-9]+,[0-9]+)\s*\(([0-9.]+)\)/);

                            if (match1) {
                                score = match1[1].replace(',', '.');
                            }
                            const match2 = fullText.match(/Calificaci[oó]n.*?([0-9]+,[0-9]+)/i);

                            if (!score && match2) {
                                score = match2[1].replace(',', '.');
                            }

                            let duration = null;

                            const durationMatch =
                                fullText.match(
                                    /([0-9]+\\s*(hora|horas|min|minutos|día|días))/
                                );

                            if (durationMatch) {

                                duration =
                                    durationMatch[1];
                            }

                            resultados.push({

                                title,

                                image,

                                score,

                                duration,

                                price,

                                numericPrice,

                                link,

                                source: 'airbnb_attractions'
                            });

                        } catch (error) {}
                    });

                    return resultados;
                }""")

                attractions_filtradas = [
                    attraction
                    for attraction in attractions
                    if attraction.get("title")
                ]

                return attractions_filtradas

            finally:

                await browser.close()