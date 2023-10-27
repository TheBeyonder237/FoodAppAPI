from pydantic import Field
from typing import Optional

from pydantic import BaseModel


class CommentSchema(BaseModel):
    user_id: str = Field(...)
    recipe_id: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "abcd1234",
                "recipe_id": "1234abcd",
                "content": "C'était délicieux !"
            }
        }


class UpdateCommentModel(BaseModel):
    content: Optional[str]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}