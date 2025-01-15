import grpc
import string
import random
from uuid import uuid4

import kody_clientsdk_python.ecom.v1.ecom_pb2 as kody_model
import kody_clientsdk_python.ecom.v1.ecom_pb2_grpc as kody_client

def send_online_payment():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your API key
    api_key = ""
    # TODO: Replace this with your amount
    amount = 314
    payment_reference = "pay_" + str(uuid4())
    # TODO: Replace this with your currency
    currency = "GBP"
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return_url = "returnUrl"
    expiry = kody_model.PaymentInitiationRequest.ExpirySettings(
        show_timer=True,
        expiring_seconds=1900
    )

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyEcomPaymentsServiceStub(channel)
        response = client.InitiatePayment(
            kody_model.PaymentInitiationRequest(
                store_id=store_id,
                payment_reference=payment_reference,
                amount=amount,
                currency=currency,
                order_id=order_id,
                return_url=return_url,
                expiry=expiry
            ),
            metadata=[("x-api-key", api_key)]
        )
    print(f"Payment ID: {response.response.payment_id}")
    print(f"Payment URL: {response.response.payment_url}")

if __name__ == "__main__":
    send_online_payment()
