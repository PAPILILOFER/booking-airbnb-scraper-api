from sqlalchemy import select

from app.domain.repositories.user_repository import UserRepository

from app.infrastructure.database.models import UserModel

class PostgresUserRepository(UserRepository):

    def __init__(self, db):
        self.db = db

    async def create_user(
        self,
        email: str,
        password: str
    ):

        user = UserModel(
            email=email,
            password=password
        )

        self.db.add(user)

        await self.db.commit()

        await self.db.refresh(user)

        return user

    async def get_by_email(
        self,
        email: str
    ):

        result = await self.db.execute(
            select(UserModel).where(
                UserModel.email == email
            )
        )

        return result.scalar_one_or_none()