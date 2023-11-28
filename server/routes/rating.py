from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_rating,
    delete_rating,
    retrieve_rating,
    retrieve_ratings,
    update_rating,
)
from server.models.rating import (
    ErrorResponseModel,
    ResponseModel,
    RatingSchema,
    UpdateRatingModel,
)

router = APIRouter()

@router.post("/", response_description="Rating data added into the database")
async def add_rating_data(rating: RatingSchema = Body(...)):
    rating = jsonable_encoder(rating)
    new_rating = await add_rating(rating)
    return ResponseModel(new_rating, "Rating added successfully.")

@router.get("/", response_description="Ratings retrieved")
async def get_ratings():
    ratings = await retrieve_ratings()
    if ratings:
        return ResponseModel(ratings, "Ratings data retrieved successfully")
    return ResponseModel(ratings, "Empty list returned")


@router.get("/{id}", response_description="Rating data retrieved")
async def get_rating_data(id):
    rating = await retrieve_rating(id)
    if rating:
        return ResponseModel(rating, "Rating data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Rating doesn't exist.")


@router.put("/{id}")
async def update_rating_data(id: str, req: UpdateRatingModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_rating = await update_rating(id, req)
    if updated_rating:
        return ResponseModel(
            "Rating with ID: {} update is successful".format(id),
            "Rating updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the rating data.",
    )


@router.delete("/{id}", response_description="Rating data deleted from the database")
async def delete_rating_data(id: str):
    deleted_rating = await delete_rating(id)
    if deleted_rating:
        return ResponseModel(
            "Rating with ID: {} removed".format(id), "Rating deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Rating with id {0} doesn't exist".format(id)
    )
