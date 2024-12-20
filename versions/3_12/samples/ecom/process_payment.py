import logging

import string
import random
from uuid import uuid4

import grpc
import kody_clientsdk_python.ecom.v1.ecom_pb2 as kody_model
import kody_clientsdk_python.ecom.v1.ecom_pb2_grpc as kody_client
from kody_clientsdk_python.sdk.common.pagination_pb2 import PageCursor

from ..config import load_config

config = load_config()


def send_online_payment():
    amount = 314
    payment_reference = "pay_" + str(uuid4())
    currency = "GBP"
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return_url = "returnUrl"
    expiry = kody_model.PaymentInitiationRequest.ExpirySettings(
        show_timer=True,
        expiring_seconds=1900
    )

    with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        kody_service = kody_client.KodyEcomPaymentsServiceStub(channel)
        response = kody_service.InitiatePayment(kody_model.PaymentInitiationRequest(store_id=config.store_id,
                                                                            payment_reference=payment_reference,
                                                                            amount=amount,
                                                                            currency=currency,
                                                                            order_id=order_id,
                                                                            return_url=return_url,
                                                                            expiry=expiry),
                                        metadata=[("x-api-key", config.api_key)])

    logging.info(f"sendOnlinePayment: response={response}")

def get_payment_details():
    #UUID
    payment_id = "" #Use an existing payment_id

    with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        kody_service = kody_client.KodyEcomPaymentsServiceStub(channel)
        response = kody_service.PaymentDetails(
            kody_model.PaymentDetailsRequest(store_id=config.store_id, payment_id = payment_id),
            metadata=[("x-api-key", config.api_key)])

    logging.info(f"getPaymentDetails: response={response}")

def get_payments():
    with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        kody_service = kody_client.KodyEcomPaymentsServiceStub(channel)
        response = kody_service.GetPayments(
            kody_model.GetPaymentsRequest(store_id=config.store_id, page_cursor=PageCursor(page_size=5)),
            metadata=[("x-api-key", config.api_key)])

    logging.info(f"getPaymentDetails: response={response}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    send_online_payment()
    get_payments()
