from datetime import datetime

from bson import ObjectId

from app.domain.ports.hotel_repository import (
    HotelRepository
)


def clean_doc(doc):

    clean = {}

    for k, v in doc.items():

        if isinstance(v, ObjectId):
            clean[k] = str(v)
        else:
            clean[k] = v

    return clean


class MongoAirbnbRepository(
    HotelRepository
):

    def __init__(self, db):

        self.collection = db.airbnb_hotels

    async def save_many(self, hotels: list):

        if not hotels:
            return

        clean_hotels = [
            {
                "title": h.get("title"),

                "location": h.get("location"),

                "image": h.get("image"),

                "score": h.get("score"),

                "numComments": h.get(
                    "numComments"
                ),

                "propertyType": h.get(
                    "propertyType"
                ),

                "price": h.get("price"),

                "link": h.get("link"),

                "source": h.get("source"),

                "scraped_at": datetime.utcnow()
            }
            for h in hotels
            if h.get("title")
        ]

        await self.collection.insert_many(
            clean_hotels
        )

    async def get_all(self):

        cursor = self.collection.find()

        hoteles = await cursor.to_list(
            length=100
        )

        return [
            clean_doc(h)
            for h in hoteles
        ]