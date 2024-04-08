from fastapi import APIRouter, Depends

from src.controllers.user import create_user, create_token
from src.dependencies.database import provide_database
from src.dto.user import LoginModel, SignUpResponse, SignUpModel
from src.security.jwt import create_jwt_token, get_jwt_payload
from src.dependencies.user import get_user_by_token

user_router = APIRouter(prefix="/user", tags=["Login"])


@user_router.post("/login", response_model=SignUpResponse)
async def login(
        payload: LoginModel,
        db=Depends(provide_database)
):
    token = await create_token(payload=payload, db=db)
    return SignUpResponse(status=True, data={"token": token})


@user_router.post("/sign-up", response_model=SignUpResponse)
async def singup(
        payload: SignUpModel,
        db=Depends(provide_database)
):
    await create_user(payload=payload, db=db)
    return SignUpResponse(status=True)
