
from typing import Optional

from pydantic import BaseModel, Field


class RatingSchema(BaseModel):
    user_id: str = Field(...)
    recipe_id: str = Field(...)
    score: int = Field(..., gt=0, lt=10)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "abcd1234",
                "recipe_id": "1234abcd",
                "score": 5
            }
        }


class UpdateRatingModel(BaseModel):
    score: Optional[int]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}