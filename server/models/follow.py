from pydantic import BaseModel, Field


class Follow(BaseModel):
    follower_id: str = Field(...)
    followed_id: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "follower_id": "sdfsdfsdfsfesf",
                "followed_id": "sdfsdfsdfsdfsdfs"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}