from datetime import datetime

from bson import ObjectId


def clean_doc(doc):

    clean = {}

    for k, v in doc.items():

        if isinstance(v, ObjectId):
            clean[k] = str(v)

        else:
            clean[k] = v

    return clean


from app.domain.ports.attraction_repository import (
    AttractionRepository
)


class MongoAttractionRepository(
    AttractionRepository
):

    def __init__(self, db):

        self.collection = db.attractions

    async def save_many(self, attractions: list):

        if not attractions:
            return

        clean_attractions = [
            {
               "description": a.get("description"),

                "duration": a.get("duration"),

                "freeCancellation": a.get(
                    "freeCancellation"
                ),

                "price": a.get("price"),

                "score": a.get("score"),

                "rating": a.get("rating"),

                "numComments": a.get(
                    "numComments"
                ),
            }

            for a in attractions
            if a.get("title")
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
            clean_doc(a)
            for a in attractions
        ]