from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr, validator


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    fullname: str = Field(...)
    bio: Optional[str] = Field(...)
    profile_image: Optional[str] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "username": "chefjohn",
                "email": "john@example.com",
                "password": "securepassword123",
                "fullname": "John Doe",
                "bio": "Passionné de cuisine depuis l'âge de 10 ans.",
                "profile_image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAU... (très longue chaîne)",
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    fullname: Optional[str]
    bio: Optional[str]
    profile_image: Optional[str]  # Données d'image en base64

    class Config:
        schema_extra = {
            "example": {
                "username": "masterchefjohn",
                "email": "john@newexample.com",
                "password": "newsecurepassword123",
                "fullname": "Johnathan Doe",
                "bio": "Ma passion pour la cuisine a commencé très tôt.",
                "profile_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD... (très longue chaîne)",
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
