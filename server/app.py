from fastapi import FastAPI

from server.routes.student import router as StudentRouter
from server.routes.user import router as UserRouter
from server.routes.payement import app as PayementRouter
from server.routes.recipe import router as RecipeRouter
from server.routes.comment import router as CommentRouter
from server.routes.category import router as CategoryRouter
from server.routes.rating import router as RatingRouter
from server.routes.favorite import router as FavoriteRouter
from server.routes.follow import router as FollowRouter
from server.routes.subscription import router as SubscriptionRouter


app = FastAPI()


app.include_router(CategoryRouter, tags=["Category"], prefix="/category")
app.include_router(CommentRouter, tags=["Comment"], prefix="/comment")
app.include_router(FavoriteRouter, tags=["Favorite"], prefix="/favorite")
app.include_router(FollowRouter, tags=["Follow"], prefix="/follow")
app.include_router(PayementRouter, tags=["Payement"], prefix="/payement")
app.include_router(RatingRouter, tags=["Rating"], prefix="/rating")
app.include_router(RecipeRouter, tags=["Recipe"], prefix="/recipe")
app.include_router(StudentRouter, tags=["Student"], prefix="/student")
app.include_router(SubscriptionRouter, tags=["Subscription"], prefix="/Subscription")
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}