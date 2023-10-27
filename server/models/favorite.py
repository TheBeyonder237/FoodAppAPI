from pydantic import BaseModel, Field
from typing import Optional


class FavoriteSchema(BaseModel):
    user_id: str = Field(...)
    recipe_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "abcd1234",
                "recipe_id": "1234abcd"
            }
        }


class UpdateFavoriteModel(BaseModel):
    user_id: Optional[str] = Field(...)
    recipe_id: Optional[str] = Field(...)


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}