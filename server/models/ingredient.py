from typing import Optional

from pydantic import BaseModel, Field


class IngredientSchema(BaseModel):
    name: str = Field(...)
    price: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Tomate",
                "price": "20100"
            }
        }


class UpdateIngredientModel(BaseModel):
    name: Optional[str]
    quantity: Optional[str]
    description: Optional[str]



def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}