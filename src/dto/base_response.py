from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: bool
    error: str | None = None
