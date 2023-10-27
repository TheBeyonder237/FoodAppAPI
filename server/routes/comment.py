from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_comment,
    delete_comment,
    retrieve_comment,
    retrieve_comments,
    update_comment,
)
from server.models.comment import (
    ErrorResponseModel,
    ResponseModel,
    CommentSchema,
    UpdateCommentModel,
)

router = APIRouter()


@router.post("/", response_description="Comment data added into the database")
async def add_comment_data(comment: CommentSchema = Body(...)):
    comment = jsonable_encoder(comment)
    new_comment = await add_comment(comment)
    return ResponseModel(new_comment, "Comment added successfully.")


@router.get("/", response_description="Comments retrieved")
async def get_comments():
    comments = await retrieve_comments()
    if comments:
        return ResponseModel(comments, "Comments data retrieved successfully")
    return ResponseModel(comments, "Empty list returned")


@router.get("/{id}", response_description="Comment data retrieved")
async def get_comment_data(id):
    comment = await retrieve_comment(id)
    if comment:
        return ResponseModel(comment, "Comment data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Comment doesn't exist.")


@router.put("/{id}")
async def update_comment_data(id: str, req: UpdateCommentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_comment = await update_comment(id, req)
    if updated_comment:
        return ResponseModel(
            "Comment with ID: {} update is successful".format(id),
            "Comment updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the comment data.",
    )


@router.delete("/{id}", response_description="Comment data deleted from the database")
async def delete_comment_data(id: str):
    deleted_comment = await delete_comment(id)
    if deleted_comment:
        return ResponseModel(
            "Comment with ID: {} removed".format(id), "Comment deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Comment with id {0} doesn't exist".format(id)
    )