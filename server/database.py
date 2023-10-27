import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.foodapp

student_collection = database.get_collection("students_collection")
user_collection = database.get_collection("users")
follow_collection = database.get_collection("follow")
recipe_collection = database.get_collection("recipes")
rating_collection = database.get_collection("rating")
category_collection = database.get_collection("category")
comment_collection = database.get_collection("comment")
ingredient_collection = database.get_collection("ingredient")
favorite_collection = database.get_collection("favorite")
payment_collection = database.get_collection("payement")
subscription_collection = database.get_collection("subscription")


# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "fullname": user["fullname"],
        "bio": user["bio"],
        "profile_image": user["profile_image"]
    }


def follow_helper(follow) -> dict:
    return {
        "id": str(follow["_id"]),
        "follower_id": follow["follower_id"],
        "followed_id": follow["followed_id"]
    }


def payment_helper(payment) -> dict:
    return {
        "id": str(payment["_id"]),
        "userEmail": payment["userEmail"],
        "paymentAmount": payment["paymentAmount"],
        "transactionId": payment["transactionId"],
        "meta": payment["meta"],
    }


def subscription_helper(subscription) -> dict:
    return {
        "id": str(subscription["_id"]),
        "user_id": subscription["user_id"],
        "start_date": subscription["start_date"],
        "end_date": subscription["end_date"],
        "is_active": subscription["is_active"],
    }


def category_helper(category) -> dict:
    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category["description"],
        "recipe_id": category["recipe_id"]
    }


def ingredient_helper(ingredient) -> dict:
    return {
        "id": str(ingredient["_id"]),
        "name": ingredient["name"],
        "quantity": ingredient["quantity"],
        "description": ingredient["description"]
    }


def recipe_helper(recipe) -> dict:
    return {
        "id": str(recipe["_id"]),
        "title": recipe["title"],
        "description": recipe["description"],
        "ingredients": recipe["ingredients"],
        "preparation_steps": recipe["preparation_steps"],
        "cooking_time": recipe["cooking_time"],
        "servings": recipe["servings"],
        "category_id": recipe["category_id"],
        "user_id": recipe["user_id"],
        "image_url": recipe["image_url"]
    }


def comment_helper(comment) -> dict:
    return {
        "id": str(comment["_id"]),
        "user_id": comment["user_id"],
        "recipe_id": comment["recipe_id"],
        "content": comment["content"]
    }


def rating_helper(rating) -> dict:
    return {
        "id": str(rating["_id"]),
        "user_id": rating["user_id"],
        "recipe_id": rating["recipe_id"],
        "score": rating["score"]
    }


def favorite_helper(favorite) -> dict:
    return {
        "id": str(favorite["_id"]),
        "user_id": favorite["user_id"],
        "recipe_id": favorite["recipe_id"]
    }


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Ensemble des fonctions CRUD pour effectuer notre travail
# Retrieve all students present in the database
async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student from the database
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True


# Pour l'utilisateur
# Add a new user into the database
# Récupérer tous les utilisateurs présents dans la base de données
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Ajouter un nouvel utilisateur à la base de données
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Récupérer un utilisateur avec un ID correspondant
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Mettre à jour un utilisateur avec un ID correspondant
async def update_user(id: str, data: dict):
    # Retourner faux si le corps de la demande est vide
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Supprimer un utilisateur de la base de données
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


# Retrieve all recipes created by a specific user
async def retrieve_recipes_by_user(user_id: str):
    recipes = []
    async for recipe in recipe_collection.find({"user_id": user_id}):
        recipes.append(recipe_helper(recipe))
    return recipes


# Retrieve all comments posted by a specific user
async def retrieve_comments_by_user(user_id: str):
    comments = []
    async for comment in comment_collection.find({"user_id": user_id}):
        comments.append(comment_helper(comment))
    return comments


# Retrieve all ratings given by a specific user
async def retrieve_ratings_by_user(user_id: str):
    ratings = []
    async for rating in rating_collection.find({"user_id": user_id}):
        ratings.append(rating_helper(rating))
    return ratings


# Retrieve all recipes favorite by a specific user
async def retrieve_favorites_by_user(user_id: str):
    favorites = []
    async for favorite in favorite_collection.find({"user_id": user_id}):
        # Here we assume the favorite object contains a recipe_id field.
        # You can retrieve the full recipe details if required.
        recipe = await recipe_collection.find_one({"_id": favorite["recipe_id"]})
        if recipe:
            favorites.append(recipe_helper(recipe))
    return favorites


# Recherche d'utilisateurs par nom, e-mail ou ID
async def search_users_by_criteria(name: str = None, email: str = None, user_id: str = None):
    query = {}
    if name:
        query["username"] = name
    if email:
        query["email"] = email
    if user_id:
        query["_id"] = ObjectId(user_id)

    users = []
    async for user in user_collection.find(query):
        users.append(user_helper(user))
    return users


# Filtrez les recettes par utilisateur
async def filter_recipes_by_user_id(user_id: str):
    recipes = []
    async for recipe in recipe_collection.find({"user_id": ObjectId(user_id)}):
        recipes.append(recipe_helper(recipe))
    return recipes


# Ensemble des fonctions CRUD pour les recettes

# Retrieve all recipes present in the database
async def retrieve_recipes():
    recipes = []
    async for recipe in recipe_collection.find():
        recipes.append(recipe_helper(recipe))
    return recipes


# Add a new recipe into the database
async def add_recipe(recipe_data: dict) -> dict:
    # Here you might want to validate if the user exists in the user collection
    recipe = await recipe_collection.insert_one(recipe_data)
    new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    return recipe_helper(new_recipe)


# Retrieve a recipe with a matching ID
async def retrieve_recipe(id: str) -> dict:
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        return recipe_helper(recipe)


# Update a recipe with a matching ID
async def update_recipe(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_recipe:
            return True
        return False


# Delete a recipe from the database
async def delete_recipe(id: str):
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})
    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True

async def retrieve_recipes_from_followed_user(followed_id: str):
    recipes = []
    async for recipe in recipe_collection.find({"followed_id": followed_id}):
        recipes.append(recipe_helper(recipe))
    return recipes


async def retrieve_recipes_by_category(category_id: str):
    recipes = []
    async for recipe in recipe_collection.find({"category_id": ObjectId(category_id)}):
        recipes.append(recipe_helper(recipe))
    return recipes


async def mark_recipe_as_favorite(user_id: str, recipe_id: str):
    favorite_data = {"user_id": ObjectId(user_id), "recipe_id": recipe_id}
    result = await favorite_collection.insert_one(favorite_data)
    return {"_id": str(result.inserted_id)}


async def retrieve_favorite_recipes(user_id: str):
    favorite_recipes = []
    async for favorite in favorite_collection.find({"user_id": user_id}):
        recipe = await recipe_collection.find_one({"_id": favorite["recipe_id"]})
        if recipe:
            favorite_recipes.append(recipe_helper(recipe))
    return favorite_recipes


# Ensemble des fonctions CRUD pour les commentaires

# Retrieve all comments present in the database
async def retrieve_comments():
    comments = []
    async for comment in comment_collection.find():
        comments.append(comment_helper(comment))
    return comments


# Add a new comment into the database
async def add_comment(comment_data: dict) -> dict:
    # Here you might want to validate if the user and the recipe both exist
    comment = await comment_collection.insert_one(comment_data)
    new_comment = await comment_collection.find_one({"_id": comment.inserted_id})
    return comment_helper(new_comment)


# Retrieve a comment with a matching ID
async def retrieve_comment(id: str) -> dict:
    comment = await comment_collection.find_one({"_id": ObjectId(id)})
    if comment:
        return comment_helper(comment)


# Update a comment with a matching ID
async def update_comment(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    comment = await comment_collection.find_one({"_id": ObjectId(id)})
    if comment:
        updated_comment = await comment_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_comment:
            return True
        return False


# Delete a comment from the database
async def delete_comment(id: str):
    comment = await comment_collection.find_one({"_id": ObjectId(id)})
    if comment:
        await comment_collection.delete_one({"_id": ObjectId(id)})
        return True


# Ensemble des fonctions CRUD pour les catégories

# Retrieve all categories present in the database
async def retrieve_categories():
    categories = []
    async for category in category_collection.find():
        categories.append(category_helper(category))
    return categories


# Add a new category into the database
async def add_category(category_data: dict) -> dict:
    category = await category_collection.insert_one(category_data)
    new_category = await category_collection.find_one({"_id": category.inserted_id})
    return category_helper(new_category)


# Retrieve a category with a matching ID
async def retrieve_category(id: str) -> dict:
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        return category_helper(category)


# Update a category with a matching ID
async def update_category(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        updated_category = await category_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_category:
            return True
        return False


# Delete a category from the database
async def delete_category(id: str):
    category = await category_collection.find_one({"_id": ObjectId(id)})
    if category:
        await category_collection.delete_one({"_id": ObjectId(id)})
        return True


#  Récupérer toutes les catégories pour une recette spécifique
async def retrieve_categories_for_recipe(recipe_id: str):
    categories = []
    async for category in category_collection.find({"recipe_id": ObjectId(recipe_id)}):
        categories.append(category_helper(category))
    return categories


#  Ajouter une catégorie à une recette
async def add_category_to_recipe(recipe_id: str, category_data: dict) -> dict:
    category_data['recipe_id'] = ObjectId(recipe_id)
    category = await category_collection.insert_one(category_data)
    new_category = await category_collection.find_one({"_id": category.inserted_id})
    return category_helper(new_category)


#  Compter le nombre de recettes pour une catégorie spécifique
async def count_recipes_for_category(category_id: str) -> int:
    count = await category_collection.count_documents({"_id": ObjectId(category_id)})
    return count


#  Vérifier si une recette est dans une catégorie spécifique
async def check_recipe_in_category(recipe_id: str, category_id: str) -> bool:
    category = await category_collection.find_one({"_id": ObjectId(category_id), "recipe_id": ObjectId(recipe_id)})
    return bool(category)


# Supprimer une recette d'une catégorie
async def delete_recipe_from_category(recipe_id: str, category_id: str):
    result = await category_collection.delete_one({"_id": ObjectId(category_id), "recipe_id": ObjectId(recipe_id)})
    return result.deleted_count > 0


#  Récupérer toutes les recettes sans catégorie
async def retrieve_recipes_without_category():
    recipes = []
    async for recipe in recipe_collection.find({"category_id": None}):
        recipes.append(recipe_helper(recipe))
    return recipes


# Ensemble des fonctions CRUD pour les évaluations

# Retrieve all ratings present in the database
async def retrieve_ratings():
    ratings = []
    async for rating in rating_collection.find():
        ratings.append(rating_helper(rating))
    return ratings


# Add a new rating into the database
async def add_rating(rating_data: dict) -> dict:
    rating = await rating_collection.insert_one(rating_data)
    new_rating = await rating_collection.find_one({"_id": rating.inserted_id})
    return rating_helper(new_rating)


# Retrieve a rating with a matching ID
async def retrieve_rating(id: str) -> dict:
    rating = await rating_collection.find_one({"_id": ObjectId(id)})
    if rating:
        return rating_helper(rating)


# Update a rating with a matching ID
async def update_rating(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    rating = await rating_collection.find_one({"_id": ObjectId(id)})
    if rating:
        updated_rating = await rating_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_rating:
            return True
        return False


# Delete a rating from the database
async def delete_rating(id: str):
    rating = await rating_collection.find_one({"_id": ObjectId(id)})
    if rating:
        await rating_collection.delete_one({"_id": ObjectId(id)})
        return True


# Ensemble des fonctions CRUD pour les favoris

# Retrieve all favorites present in the database
async def retrieve_favorites():
    favorites = []
    async for favorite in favorite_collection.find():
        favorites.append(favorite_helper(favorite))
    return favorites


# Add a new favorite into the database
async def add_favorite(favorite_data: dict) -> dict:
    favorite = await favorite_collection.insert_one(favorite_data)
    new_favorite = await favorite_collection.find_one({"_id": favorite.inserted_id})
    return favorite_helper(new_favorite)


# Retrieve a favorite with a matching ID
async def retrieve_favorite(id: str) -> dict:
    favorite = await favorite_collection.find_one({"_id": ObjectId(id)})
    if favorite:
        return favorite_helper(favorite)


# Update a favorite with a matching ID
async def update_favorite(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    favorite = await favorite_collection.find_one({"_id": ObjectId(id)})
    if favorite:
        updated_favorite = await favorite_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_favorite:
            return True
        return False


# Delete a favorite from the database
async def delete_favorite(id: str):
    favorite = await favorite_collection.find_one({"_id": ObjectId(id)})
    if favorite:
        await favorite_collection.delete_one({"_id": ObjectId(id)})
        return True


# Ensemble des fonctions CRUD pour "follow"

# Create a new follow relationship
async def add_follow(follow_data: dict) -> dict:
    follow = await follow_collection.insert_one(follow_data)
    new_follow = await follow_collection.find_one({"_id": follow.inserted_id})
    return new_follow


# Retrieve a specific follow relationship by its ID
async def retrieve_follow(follow_id: str) -> dict:
    follow = await follow_collection.find_one({"_id": ObjectId(follow_id)})
    return follow


# Retrieve all users followed by a specific user
async def retrieve_followed_by_user(follower_id: str):
    followed_users = []
    async for follow in follow_collection.find({"follower_id": follower_id}):
        followed_users.append(follow['followed_id'])
    return followed_users


# Retrieve all followers of a specific user
async def retrieve_followers_of_user(followed_id: str):
    followers = []
    async for follow in follow_collection.find({"followed_id": followed_id}):
        followers.append(follow['follower_id'])
    return followers


# Delete a follow relationship
async def unfollow(follow_id: str):
    result = await follow_collection.delete_one({"_id": ObjectId(follow_id)})
    return result.deleted_count > 0


# Ensemble des fonctions CRUD pour les paiements

# Retrieve all payments present in the database
async def retrieve_payments():
    payments = []
    async for payment in payment_collection.find():
        payments.append(payment_helper(payment))
    return payments


# Add a new payment into the database
async def add_payment(payment_data: dict) -> dict:
    payment = await payment_collection.insert_one(payment_data)
    new_payment = await payment_collection.find_one({"_id": payment.inserted_id})
    return payment_helper(new_payment)


# Retrieve a payment with a matching ID
async def retrieve_payment(id: str) -> dict:
    payment = await payment_collection.find_one({"_id": ObjectId(id)})
    if payment:
        return payment_helper(payment)


# Update a payment with a matching ID
async def update_payment(id: str, data: dict):
    if len(data) < 1:
        return False
    payment = await payment_collection.find_one({"_id": ObjectId(id)})
    if payment:
        updated_payment = await payment_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_payment:
            return True
        return False


# Delete a payment from the database
async def delete_payment(id: str):
    payment = await payment_collection.find_one({"_id": ObjectId(id)})
    if payment:
        await payment_collection.delete_one({"_id": ObjectId(id)})
        return True


# Retrieve all subscriptions present in the database
async def retrieve_subscriptions():
    subscriptions = []
    async for subscription in subscription_collection.find():
        subscriptions.append(subscription_helper(subscription))
    return subscriptions


# Add a new subscription into the database
async def add_subscription(subscription_data: dict) -> dict:
    subscription = await subscription_collection.insert_one(subscription_data)
    new_subscription = await subscription_collection.find_one({"_id": subscription.inserted_id})
    return subscription_helper(new_subscription)


# Retrieve a subscription with a matching ID
async def retrieve_subscription(id: str) -> dict:
    subscription = await subscription_collection.find_one({"_id": ObjectId(id)})
    if subscription:
        return subscription_helper(subscription)


# Update a subscription with a matching ID
async def update_subscription(id: str, data: dict):
    if len(data) < 1:
        return False
    subscription = await subscription_collection.find_one({"_id": ObjectId(id)})
    if subscription:
        updated_subscription = await subscription_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_subscription:
            return True
        return False


# Delete a subscription from the database
async def delete_subscription(id: str):
    subscription = await subscription_collection.find_one({"_id": ObjectId(id)})
    if subscription:
        await subscription_collection.delete_one({"_id": ObjectId(id)})
        return True


async def add_subscription_after_payment(payment: dict):
    subscription_data = {
        "user_id": payment["user_id"],
        "start_date": ... ,  # the start date logic
        "end_date": ... ,    # the end date logic
        "is_active": True
    }
    await subscription_collection.insert_one(subscription_data)