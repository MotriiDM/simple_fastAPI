from typing import Dict, Optional, List

from pydantic import BaseModel, constr

from src.dto.base_response import BaseResponse


class CreatePostModel(BaseModel):
    text: constr(min_length=1, max_length=1024)


class ResponseCreatedPostModel(BaseResponse):
    data: Dict | None = None


class ResponsePostsModel(BaseResponse):
    data: List
