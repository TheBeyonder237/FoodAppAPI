from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_favorite,
    delete_favorite,
    retrieve_favorite,
    retrieve_favorites,
    update_favorite,
)
from server.models.favorite import (
    ErrorResponseModel,
    ResponseModel,
    FavoriteSchema,
    UpdateFavoriteModel,
)

router = APIRouter()

@router.post("/", response_description="Favorite data added into the database")
async def add_favorite_data(favorite: FavoriteSchema = Body(...)):
    favorite = jsonable_encoder(favorite)
    new_favorite = await add_favorite(favorite)
    return ResponseModel(new_favorite, "Favorite added successfully.")

@router.get("/", response_description="Favorites retrieved")
async def get_favorites():
    favorites = await retrieve_favorites()
    if favorites:
        return ResponseModel(favorites, "Favorites data retrieved successfully")
    return ResponseModel(favorites, "Empty list returned")

@router.get("/{id}", response_description="Favorite data retrieved")
async def get_favorite_data(id):
    favorite = await retrieve_favorite(id)
    if favorite:
        return ResponseModel(favorite, "Favorite data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Favorite doesn't exist.")

@router.put("/{id}")
async def update_favorite_data(id: str, req: UpdateFavoriteModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_favorite = await update_favorite(id, req)
    if updated_favorite:
        return ResponseModel(
            "Favorite with ID: {} update is successful".format(id),
            "Favorite updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the favorite data.",
    )

@router.delete("/{id}", response_description="Favorite data deleted from the database")
async def delete_favorite_data(id: str):
    deleted_favorite = await delete_favorite(id)
    if deleted_favorite:
        return ResponseModel(
            "Favorite with ID: {} removed".format(id), "Favorite deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Favorite with id {0} doesn't exist".format(id)
    )