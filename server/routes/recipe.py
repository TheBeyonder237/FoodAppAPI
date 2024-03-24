from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    retrieve_recipes,
    retrive_recipe_with_price,
    update_recipe,
    retrieve_favorite_recipes,
    retrieve_recipes_from_followed_user,
    retrieve_recipes_by_category,
    mark_recipe_as_favorite
)

from server.models.recipe import (
    ErrorResponseModel,
    ResponseModel,
    RecipeSchema,
    UpdateRecipeModel,
)

router = APIRouter()


@router.post("/", response_description="Recipe data added into the database")
async def add_recipe_data(recipe: RecipeSchema = Body(...)):
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(recipe)
    return ResponseModel(new_recipe, "Recipe added successfully.")


@router.get("/", response_description="Recipes retrieved")
async def get_recipes():
    recipes = await retrieve_recipes()
    if recipes:
        return ResponseModel(recipes, "Recipes data retrieved successfully")
    return ResponseModel(recipes, "Empty list returned")


@router.get("/{title}", response_description="Recipe data retrieved")
async def get_recipe_data(title):
    recipe = await retrieve_recipe(title)
    if recipe:
        return ResponseModel(recipe, "Recipe data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Recipe doesn't exist.")


@router.put("/{id}")
async def update_recipe_data(id: str, req: UpdateRecipeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_recipe = await update_recipe(id, req)
    if updated_recipe:
        return ResponseModel(
            "Recipe with ID: {} update is successful".format(id),
            "Recipe updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the recipe data.",
    )


@router.delete("/{id}", response_description="Recipe data deleted from the database")
async def delete_recipe_data(id: str):
    deleted_recipe = await delete_recipe(id)
    if deleted_recipe:
        return ResponseModel(
            "Recipe with ID: {} removed".format(id), "Recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Recipe with id {0} doesn't exist".format(id)
    )


@router.get("/from-followed/{followed_user_id}", response_description="Retrieve recipes from followed user")
async def get_recipes_from_followed_user(followed_id: str):
    recipes = await retrieve_recipes_from_followed_user(followed_id)
    return ResponseModel(recipes, "Recipes from followed user retrieved successfully.")


@router.get("/by-category/{category_id}", response_description="Retrieve recipes by category")
async def get_recipes_by_category(category_id: str):
    recipes = await retrieve_recipes_by_category(category_id)
    return ResponseModel(recipes, "Recipes by category retrieved successfully.")


@router.post("/favorite/{recipe_id}", response_description="Mark recipe as favorite")
async def favorite_recipe(recipe_id: str, user_id: str):  # assuming user_id is passed, adjust authentication as needed
    result = await mark_recipe_as_favorite(user_id, recipe_id)
    return ResponseModel(result, "Recipe marked as favorite successfully.")


@router.get("/favorites/{user_id}", response_description="Retrieve favorite recipes of a user")
async def get_favorite_recipes(user_id: str):
    recipes = await retrieve_favorite_recipes(user_id)
    return ResponseModel(recipes, "Favorite recipes retrieved successfully.")