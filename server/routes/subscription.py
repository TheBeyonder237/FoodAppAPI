from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_subscription,
    search_users_by_criteria,
    delete_subscription,
    retrieve_subscriptions,
    update_subscription,
    retrieve_subscription,
    retrieve_recipes_from_followed_user,
    add_subscription_after_payment,

)

from server.models.subscription import (
    ErrorResponseModel,
    ResponseModel,
    UpdateSubscriptionSchema,
    SubscriptionSchema,
)


router = APIRouter()


# Créer un nouvel abonnement
@router.post("/subscriptions/")
async def create_subscription(subscription: SubscriptionSchema):
    new_subscription = await add_subscription(subscription.dict())
    if new_subscription:
        return ResponseModel(new_subscription, "Subscription created successfully.")
    return ErrorResponseModel("An error occurred.", 400, "Subscription was not created.")


# Récupérer tous les abonnements
@router.get("/subscriptions/")
async def list_subscriptions():
    subscriptions = await retrieve_subscriptions()
    if subscriptions:
        return ResponseModel(subscriptions, "Subscriptions data retrieved successfully")
    return ResponseModel(subscriptions, "Empty list returned")


# Récupérer un abonnement spécifique
@router.get("/subscriptions/{subscription_id}")
async def get_subscription(subscription_id: str):
    subscription = await retrieve_subscription(subscription_id)
    if subscription:
        return ResponseModel(subscription, "Subscription data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Subscription doesn't exist.")


# Mettre à jour un abonnement
@router.put("/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: str, req: UpdateSubscriptionSchema):
    req_data = {k: v for k, v in req.dict().items() if v is not None}
    updated_subscription = await update_subscription(subscription_id, req_data)
    if updated_subscription:
        return ResponseModel(
            "Subscription with ID: {} update is successful".format(subscription_id),
            "Subscription updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the subscription data.",
    )


# Supprimer un abonnement
@router.delete("/subscriptions/{subscription_id}")
async def delete_subscription(subscription_id: str):
    deleted_subscription = await delete_subscription(subscription_id)
    if deleted_subscription:
        return ResponseModel(
            "Subscription with ID: {} removed".format(subscription_id), "Subscription deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Subscription with id {0} doesn't exist".format(subscription_id)
    )