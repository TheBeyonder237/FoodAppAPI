import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from server.database import retrieve_payment, update_payment, add_subscription_after_payment
from server.models.payement import PaymentInput, PaymentOutput
import httpx
import os

app = APIRouter()

endpointUrl = "https://api.notchpay.co/payments/initialize"
cb_url = os.getenv("REDIRECT_URL")

NOTCHPAY_API_URL = "https://api.notchpay.co"
API_KEY = "sb.H8EcJQBr30HIIwM6bSt8KeHqHRl0OWPTgZRvUNmfwXnW5Yrod7Yl58Fdao4KldV00jLYGdNzcKTZZjQIVPyBk5iyrx2zAhoq4bKquFJqtqagAc7UMab5cC9CTuSYM"
REDIRECT_URL = "https://api.notchpay.co/payments/"


async def get_api_key():
    if not API_KEY:
        raise HTTPException(status_code=400, detail="API Key not found")
    return API_KEY


@app.post("/initialize_payment/")
async def initialize_payment(
    user_id: str, userEmail: str, paymentAmount: float, apiKey: str = Depends(get_api_key)
):
    paymentRequest = {
        "email": userEmail,
        "amount": paymentAmount,
        "currency": "XAF",
        "description": "Payment for Subscription",
        "callback": f"{REDIRECT_URL}?tid={user_id}",
    }

    headers = {
        "Authorization": apiKey,
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(NOTCHPAY_API_URL + "/payments/initialize", json=paymentRequest, headers=headers)
            response.raise_for_status()

            paymentLink = response.json().get("transaction", {}).get("reference")
            if paymentLink:
                return {"payment_link": f"https://pay.notchpay.co/{paymentLink}"}
            else:
                return {"error": f"Error initiating the transaction on NOTCHPAY: {response.text}"}

        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP ERROR: {exc.response.status_code}", "details": exc.response.text}
        except Exception as e:
            return {"error": f"UNKNOWN ERROR: {str(e)}"}


@app.get("/verify_payment/")
async def verify_payment_status(transaction_id: str) -> dict:
    endpoint = f"/payments/{transaction_id}"
    headers = {"Authorization": API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOTCHPAY_API_URL}{endpoint}", headers=headers)
        if 200 <= response.status_code < 300:
            return {"status": True, "transaction": response.json()}
        else:
            return {"status": None}


@app.get("/payment_callback/")
async def callback_handler(request: Request):
    body = await request.body()
    signature = hmac.new(bytes(API_KEY, 'utf-8'), msg=body, digestmod=hashlib.sha256).hexdigest()
    received_signature = request.headers.get("x-notch-signature")
    if signature != received_signature:
        raise HTTPException(status_code=403, detail="Invalid signature")

    transaction_id = request.query_params.get("tid")
    print(transaction_id)
    payment = await retrieve_payment(transaction_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Transaction Not Found")
    if payment["status"] in ["complete", "canceled", "failed"]:
        return {"message": "Webhook received and processed successfully"}

    reference = request.query_params.get("reference")
    payment_object = await verify_payment_status(reference)
    if payment_object["status"] is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Provider server not available",
                "data": payment_object.get("transaction")
            }
        )

    updated = await update_payment(transaction_id, {"status": payment_object["transaction"]["transaction"]["status"]})
    if updated and payment_object["transaction"]["transaction"]["status"] == "successful":
        await add_subscription_after_payment(payment)

    return {"message": "Webhook processed successfully"}
