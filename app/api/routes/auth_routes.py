from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db

from app.auth.schemas import (
    RegisterSchema,
    LoginSchema
)

from app.infrastructure.persistence.postgres_user_repository import (
    PostgresUserRepository
)

from app.application.register_user import (
    RegisterUserUseCase
)

from app.application.login_user import (
    LoginUserUseCase
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
async def register(
    data: RegisterSchema,
    db: AsyncSession = Depends(get_db)
):

    repository = PostgresUserRepository(db)

    use_case = RegisterUserUseCase(repository)

    return await use_case.execute(
        email=data.email,
        password=data.password
    )


@router.post("/login")
async def login(
    data: LoginSchema,
    db: AsyncSession = Depends(get_db)
):

    repository = PostgresUserRepository(db)

    use_case = LoginUserUseCase(repository)

    return await use_case.execute(
        email=data.email,
        password=data.password
    )