import random
import os
from dotenv import load_dotenv
load_dotenv()
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
from playwright.async_api import (
    async_playwright
)

from app.domain.ports.attraction_scraper_port import AttractionScraperPort

class PlaywrightBookingAttractionsScraper(
     AttractionScraperPort
):

    async def scrape_attractions(self):

        url = (
            "https://www.booking.com/"
            "attractions/searchresults.es.html"
            "?selected_currency=COP"
            "&dest_id=-343779"
        )

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                 headless= HEADLESS,
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

                for _ in range(8):

                    await page.evaluate(
                        "window.scrollBy(0, 1200)"
                    )

                    await page.wait_for_timeout(
                        random.randint(1500, 2500)
                    )

                attractions = await page.evaluate("""() => {

                                    return Array.from(document.querySelectorAll('[data-testid="card"]')).map(card => {
                        const titleElement = card.querySelector('[data-testid="card-title"]');
                        const title = titleElement?.textContent?.trim() || null;
                        
                        const linkElement = card.querySelector('a[href*="attractions"]');
                        const link = linkElement ? linkElement.href : null;
                    
                        const location = titleElement?.closest('div')?.nextElementSibling?.textContent?.trim() || null;

                        const image = card.querySelector('img')?.src || null;

                        const description = titleElement?.closest('div')?.nextElementSibling?.nextElementSibling?.textContent?.trim() || null;

                        const freeCancellationElement = Array.from(card.querySelectorAll('span, div'))
                            .find(el => el.children.length === 0 && el.textContent.includes('Cancelación gratis'));
                        const freeCancellation = freeCancellationElement ? freeCancellationElement.textContent.trim() : null;

                        const durationElement = Array.from(card.querySelectorAll('span, div'))
                            .find(el => el.children.length === 0 && el.textContent.includes('Duración'));
                        const duration = durationElement ? durationElement.textContent.replace(/Duración:\s*/i, '').trim() : null;

                        const priceContainer = card.querySelector('[data-testid="price"]');
                        let price = null;
                        if (priceContainer) {
                            // Extraemos limpiamente el formato "COP 1.116.984" usando una expresión regular sobre todo el texto del bloque
                            const match = priceContainer.textContent.match(/COP\s*[0-9.]+/);
                            price = match ? match[0] : null;
                        }

                        const reviewBox = card.querySelector('[data-testid="review-score"]');
                        
                        const altReviewBox = reviewBox || Array.from(card.querySelectorAll('div, span')).find(el => el.textContent.includes('comentario'));

                        let score = null;
                        let rating = null;
                        let numComments = null;

                        if (altReviewBox) {
                            const scoreMatch = altReviewBox.textContent.match(/^([0-9.,]+)/);
                            score = scoreMatch ? scoreMatch[1].replace(',', '.') : null;

                            if (altReviewBox.textContent.includes('Excepcional')) rating = 'Excepcional';
                            else if (altReviewBox.textContent.includes('Excelente')) rating = 'Excelente';
                            else if (altReviewBox.textContent.includes('Muy bien')) rating = 'Muy bien';

                            const commentsMatch = altReviewBox.textContent.match(/([0-9.]+)\s*comentario/i);
                            numComments = commentsMatch ? commentsMatch[1] : null;
                        }

                        return {
                            title,
                            location,
                            image,
                            description,
                            duration,
                            freeCancellation,
                            price,
                            score,
                            rating,
                            numComments,
                            link,
                            source: 'booking_attractions'
                        };
                    });
                }""")

                attractions_filtered = [
                    attraction
                    for attraction in attractions
                    if attraction.get("title")
                ]

                return attractions_filtered

            finally:

                await browser.close()