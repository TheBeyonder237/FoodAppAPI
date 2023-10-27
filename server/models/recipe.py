from pydantic import BaseModel, Field
from typing import Optional, List
from server.models.ingredient import IngredientSchema


class RecipeSchema(BaseModel):
    title: str = Field(...)
    description: Optional[str]
    ingredients: List[IngredientSchema]
    preparation_steps: List[str] = Field(...)
    cooking_time: int = Field(...)
    servings: int = Field(...)
    category_id: str = Field(...)
    user_id: str = Field(...)
    image_url: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Salade César",
                "description": "Une salade classique et rafraîchissante",
                "ingredients": [{"name": "Laitue", "quantity": "1", "description": "Grande"}],
                "preparation_steps": ["Laver la laitue", "Mélanger tous les ingrédients"],
                "cooking_time": 15,
                "servings": 2,
                "category_id": "1234abcd",
                "user_id": "abcd1234",
                "image_url": "url/to/image.jpg"
            }
        }


class UpdateRecipeModel(BaseModel):
    title: Optional[str]
    description: Optional[str]
    ingredients: Optional[List[IngredientSchema]]
    preparation_steps: Optional[List[str]]
    cooking_time: Optional[int]
    servings: Optional[int]
    category_id: Optional[str]
    user_id: Optional[str]
    image_url: Optional[str]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
