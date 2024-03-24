from fastapi import APIRouter, Body, Query
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
    retrieve_recipes_by_user,
    retrieve_comments_by_user,
    retrieve_ratings_by_user,
    retrieve_favorites_by_user,
    search_users_by_criteria,
    filter_recipes_by_user_id
)
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{email}", response_description="User data retrieved")
async def get_user_data(email):
    user = await retrieve_user(email)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} update is successful".format(id),
            "User updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )


# Routes pour les recettes créées par un utilisateur spécifique
@router.get("/recipes/user/{user_id}", response_description="Retrieve recipes by a specific user")
async def get_recipes_by_user(user_id: str):
    recipes = await retrieve_recipes_by_user(user_id)
    if recipes:
        return ResponseModel(recipes, "Recipes retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No recipes found for this user.")


# Routes pour les commentaires postés par un utilisateur
@router.get("/comments/user/{user_id}", response_description="Retrieve comments by a specific user")
async def get_comments_by_user(user_id: str):
    comments = await retrieve_comments_by_user(user_id)
    if comments:
        return ResponseModel(comments, "Comments retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No comments found for this user.")


# Routes pour les évaluations données par un utilisateur
@router.get("/ratings/user/{user_id}", response_description="Retrieve ratings by a specific user")
async def get_ratings_by_user(user_id: str):
    ratings = await retrieve_ratings_by_user(user_id)
    if ratings:
        return ResponseModel(ratings, "Ratings retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No ratings found for this user.")


# Routes pour les recettes mises en favori par un utilisateur
@router.get("/favorites/user/{user_id}", response_description="Retrieve favorited recipes by a specific user")
async def get_favorites_by_user(user_id: str):
    favorites = await retrieve_favorites_by_user(user_id)
    if favorites:
        return ResponseModel(favorites, "Favorites retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No favorites found for this user.")


# Route pour rechercher des utilisateurs par nom, e-mail ou ID
@router.get("/search/users", response_description="Search for users")
async def search_for_users(name: str = Query(None), email: str = Query(None), user_id: str = Query(None)):
    users = await search_users_by_criteria(name, email, user_id)
    if users:
        return ResponseModel(users, "Users retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No users found.")

# Route pour filtrer les recettes par utilisateur
@router.get("/recipes/user/{user_id}", response_description="Filter recipes by user")
async def get_recipes_by_user(user_id: str):
    recipes = await filter_recipes_by_user_id(user_id)
    if recipes:
        return ResponseModel(recipes, "Recipes retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No recipes found for this user.")