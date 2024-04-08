from typing import Any, Dict

from pydantic import BaseModel

from src.dto.base_response import BaseResponse


class LoginModel(BaseModel):
    login: str
    password: str


class SignUpModel(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class SignUpResponse(BaseResponse):
    data: Dict | None = None
