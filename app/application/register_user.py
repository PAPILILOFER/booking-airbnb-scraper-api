from fastapi import HTTPException

from app.domain.repositories.user_repository import UserRepository

from app.auth.password_handler import hash_password

class RegisterUserUseCase:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    async def execute(
        self,
        email: str,
        password: str
    ):

        existing_user = await self.repository.get_by_email(
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Usuario ya existe"
            )

        hashed_password = hash_password(password)

        user = await self.repository.create_user(
            email=email,
            password=hashed_password
        )

        return {
            "id": user.id,
            "email": user.email
        }