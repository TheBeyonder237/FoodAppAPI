from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubscriptionSchema(BaseModel):
    transaction_id: str
    user_id: str
    start_date: datetime
    end_date: datetime
    is_active: bool = False

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "p.hbYyCrmOwoFh1lY8kZE47XgG4y5sNNV1T7K6DunOqGxyaVHVvJ2Dd6VVW4uRgD9F9Zxy2GtyKWZSUllIRuVezot9XQO6q2Ck",
                "user_id": "6538eae0ca451876b30dd57e",
                "star_date": "2002-10-30 12:00:00",
                "end_date": "2022-11-29 12:00:00",
                "is_active": False,
            }
        }


class UpdateSubscriptionSchema(BaseModel):
    transaction_id: Optional[str]
    user_id: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    is_active: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "transaction_id": "p.hbYyCrmOwoFh1lY8kZE47XgG4y5sNNV1T7K6DunOqGxyaVHVvJ2Dd6VVW4uRgD9F9Zxy2GtyKWZSUllIRuVezot9XQO6q2Ck",
                "user_id": "6538eae0ca451876b30dd57e",
                "star_date": "2002-10-30 12:00:00",
                "end_date": "2022-11-29 12:00:00",
                "is_active": False,
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