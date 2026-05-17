from fastapi import HTTPException

from app.domain.repositories.user_repository import UserRepository

from app.auth.password_handler import verify_password

from app.auth.jwt_handler import create_access_token

class LoginUserUseCase:

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

        user = await self.repository.get_by_email(
            email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Credenciales inválidas"
            )

        token = create_access_token({
            "sub": str(user.id),
            "email": user.email
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }