from pydantic import BaseModel


class PaymentInput(BaseModel):
    userEmail: str
    paymentAmount: float
    transactionId: str
    meta: dict


class PaymentOutput(BaseModel):
    payment_link: str = None
    error: str = None


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}