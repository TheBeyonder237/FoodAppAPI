from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_category,
    delete_category,
    retrieve_category,
    retrieve_categories,
    update_category, retrieve_recipes_without_category, delete_recipe_from_category, check_recipe_in_category,
    count_recipes_for_category, retrieve_categories_for_recipe, add_category_to_recipe,
)
from server.models.category import (
    ErrorResponseModel,
    ResponseModel,
    CategorySchema,
    UpdateCategoryModel,
)

router = APIRouter()


@router.post("/", response_description="Category data added into the database")
async def add_category_data(category: CategorySchema = Body(...)):
    category = jsonable_encoder(category)
    new_category = await add_category(category)
    return ResponseModel(new_category, "Category added successfully.")


@router.get("/", response_description="Categories retrieved")
async def get_categories():
    categories = await retrieve_categories()
    if categories:
        return ResponseModel(categories, "Categories data retrieved successfully")
    return ResponseModel(categories, "Empty list returned")


@router.get("/{id}", response_description="Category data retrieved")
async def get_category_data(id):
    category = await retrieve_category(id)
    if category:
        return ResponseModel(category, "Category data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Category doesn't exist.")


@router.put("/{id}")
async def update_category_data(id: str, req: UpdateCategoryModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_category = await update_category(id, req)
    if updated_category:
        return ResponseModel(
            "Category with ID: {} update is successful".format(id),
            "Category updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the category data.",
    )


@router.delete("/{id}", response_description="Category data deleted from the database")
async def delete_category_data(id: str):
    deleted_category = await delete_category(id)
    if deleted_category:
        return ResponseModel(
            "Category with ID: {} removed".format(id), "Category deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Category with id {0} doesn't exist".format(id)
    )


# Récupérer toutes les catégories pour une recette spécifique
@router.get("/recipe/{recipe_id}/categories", response_description="Categories retrieved for a specific recipe")
async def get_categories_for_recipe(recipe_id: str):
    categories = await retrieve_categories_for_recipe(recipe_id)
    if categories:
        return ResponseModel(categories, "Categories retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No categories found for this recipe.")


# Ajouter une catégorie à une recette
@router.post("/recipe/{recipe_id}/category", response_description="Category added to a specific recipe")
async def add_new_category_to_recipe(recipe_id: str, category: CategorySchema = Body(...)):
    category = jsonable_encoder(category)
    new_category = await add_category_to_recipe(recipe_id, category)
    return ResponseModel(new_category, "Category added to recipe successfully.")


# Compter le nombre de recettes pour une catégorie spécifique
@router.get("/category/{category_id}/recipe_count", response_description="Number of recipes for a specific category")
async def get_recipe_count_for_category(category_id: str):
    count = await count_recipes_for_category(category_id)
    return ResponseModel(count, f"There are {count} recipes for this category.")


# Vérifier si une recette est dans une catégorie spécifique
@router.get("/recipe/{recipe_id}/category/{category_id}", response_description="Check if recipe is in a specific "
                                                                               "category")
async def is_recipe_in_category(recipe_id: str, category_id: str):
    is_present = await check_recipe_in_category(recipe_id, category_id)
    if is_present:
        return ResponseModel(True, "Recipe is present in the category.")
    return ErrorResponseModel("An error occurred.", 404, "Recipe is not present in the category.")


#  Supprimer une recette d'une catégorie
@router.delete("/recipe/{recipe_id}/category/{category_id}", response_description="Recipe removed from a specific "
                                                                                  "category")
async def remove_recipe_from_category(recipe_id: str, category_id: str):
    is_removed = await delete_recipe_from_category(recipe_id, category_id)
    if is_removed:
        return ResponseModel(is_removed, "Recipe removed from the category successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Recipe couldn't be removed from the category.")


# Récupérer toutes les recettes sans catégorie
@router.get("/recipes_without_category", response_description="Recipes without a category retrieved")
async def get_recipes_without_any_category():
    recipes = await retrieve_recipes_without_category()
    if recipes:
        return ResponseModel(recipes, "Recipes without a category retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No recipes found without a category.")
