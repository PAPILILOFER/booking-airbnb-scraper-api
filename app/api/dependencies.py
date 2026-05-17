from app.infrastructure.database.postgres import (
    AsyncSessionLocal
)

from app.infrastructure.database.mongo import (
    get_mongo_database
)


async def get_db():

    async with AsyncSessionLocal() as session:
        yield session


def get_mongo_db():

    return get_mongo_database()