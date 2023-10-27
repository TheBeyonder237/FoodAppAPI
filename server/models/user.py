from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# Modèle principal de l'utilisateur
class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    fullname: str = Field(...)
    bio: Optional[str] = Field(...)
    profile_image: Optional[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "chefjohn",
                "email": "[email protected]",
                "password": "securepassword123",
                "fullname": "John Doe",
                "bio": "Passionné de cuisine depuis l'âge de 10 ans.",
                "profile_image": "url/to/profile/image.jpg",
            }
        }


# Modèle pour mettre à jour l'utilisateur
class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    fullname: Optional[str]
    bio: Optional[str]
    profile_image: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "masterchefjohn",
                "email": "[email protected]",
                "password": "newsecurepassword123",
                "fullname": "Johnathan Doe",
                "bio": "Ma passion pour la cuisine a commencé très tôt.",
                "profile_image": "url/to/new/profile/image.jpg",
            }
        }


# Modèles de réponse
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
