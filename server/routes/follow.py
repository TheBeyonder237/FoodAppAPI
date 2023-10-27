from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_follow,
    retrieve_followed_by_user,
    retrieve_followers_of_user,
    unfollow,
)
from server.models.follow import (Follow, ErrorResponseModel, ResponseModel)

router = APIRouter()


# Route pour suivre un autre utilisateur
@router.post("/follow", response_description="User followed successfully")
async def follow_user(follow: Follow = Body(...)):
    follow = jsonable_encoder(follow)
    new_follow = await add_follow(follow)
    return ResponseModel(new_follow, "User followed successfully.")


# Route pour obtenir la liste des utilisateurs suivis par un utilisateur spécifique
@router.get("/followed/{follower_id}", response_description="Retrieve followed users by a specific user")
async def get_followed_by_user(follower_id: str):
    followed_users = await retrieve_followed_by_user(follower_id)
    if followed_users:
        return ResponseModel(followed_users, "Followed users retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No followed users found for this user.")


# Route pour obtenir la liste des abonnés d'un utilisateur spécifique
@router.get("/followers/{followed_id}", response_description="Retrieve followers of a specific user")
async def get_followers_of_user(followed_id: str):
    followers = await retrieve_followers_of_user(followed_id)
    if followers:
        return ResponseModel(followers, "Followers retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "No followers found for this user.")


# Route pour annuler le suivi d'un autre utilisateur
@router.delete("/unfollow/{follow_id}", response_description="Unfollowed successfully")
async def unfollow_user(follow_id: str):
    result = await unfollow(follow_id)
    if result:
        return ResponseModel(follow_id, "User unfollowed successfully.")
    return ErrorResponseModel("An error occurred.", 404, "Failed to unfollow the user.")
