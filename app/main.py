import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from fastapi import FastAPI

from app.infrastructure.database.postgres import engine, Base

from app.api.routes.auth_routes import router as auth_router
from app.api.routes.scraper_routes import router as scraper_router

app = FastAPI()


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)
app.include_router(scraper_router)
