import logging

from typing import Any, Dict

from jose import jwt

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status
from starlette.exceptions import HTTPException

auth_scheme = HTTPBearer(scheme_name="User JWT token", bearerFormat="JWT")


def get_jwt_payload(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, "secret-key", algorithms=["HS256"])
    except jwt.JWTError as e:
        logging.warning("JWT validate error, %s, token=%s", e, token)
        credentials_exception.detail = "Bad JWT token"
        raise credentials_exception
    return payload


async def create_jwt_token(credentials):
    return jwt.encode(credentials, "secret-key", algorithm="HS256")
