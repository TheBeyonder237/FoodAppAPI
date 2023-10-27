from typing import Optional

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    name: str = Field(...)
    description: Optional[str]
    recipe_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Desserts",
                "description": "Toutes sortes de douceurs pour terminer le repas."
            }
        }
        

class UpdateCategoryModel(BaseModel):
    name: Optional[str]
    description: Optional[str]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}