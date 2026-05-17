from datetime import datetime
from bson import ObjectId

from app.domain.ports.airbnb_attraction_repository import AirbnbAttractionRepository


def clean_doc(doc):

    clean = {}

    for k, v in doc.items():

        if isinstance(v, ObjectId):
            clean[k] = str(v)
        else:
            clean[k] = v

    return clean


class MongoAirbnbAttractionRepository(
    AirbnbAttractionRepository
):

    def __init__(self, db):

        self.collection = db.airbnb_attractions

    async def save_many(
        self,
        attractions: list
    ):

        if not attractions:
            return

        clean_attractions = [

            {
                "title": e.get("title"),
                "image": e.get("image"),
                "score": e.get("score"),
                "duration": e.get("duration"),
                "price": e.get("price"),
                "numericPrice": e.get("numericPrice"),
                "link": e.get("link"),
                "source": e.get("source"),
                "scraped_at": datetime.utcnow()
            }

            for e in attractions
            if e.get("title")
        ]

        await self.collection.insert_many(
            clean_attractions
        )

    async def get_all(self):

        cursor = self.collection.find()

        attractions = await cursor.to_list(
            length=100
        )

        return [
            clean_doc(e)
            for e in attractions
        ]