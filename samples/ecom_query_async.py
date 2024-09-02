import logging

import asyncio
import string
import random
from uuid import uuid4

import grpc
import kody_clientsdk_python.ecom.v1.ecom_pb2 as ecom_model
import kody_clientsdk_python.ecom.v1.ecom_pb2_grpc as ecom_grpc_client
from kody_clientsdk_python.sdk.common.pagination_pb2 import PageCursor

from samples.config import load_config

config = load_config()

async def send_online_payment_async() -> None:
    amount = 314
    payment_reference = "pay_" + str(uuid4())
    currency = "GBP"
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return_url = "returnUrl"

    async with grpc.aio.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = ecom_grpc_client.KodyEcomPaymentsServiceStub(channel)
        response = await stub.InitiatePayment(ecom_model.PaymentInitiationRequest(store_id=config.store_id,
                                                                            payment_reference=payment_reference,
                                                                            amount=amount,
                                                                            currency=currency,
                                                                            order_id=order_id,
                                                                            return_url=return_url),
                                        metadata=[("x-api-key", config.api_key)])

        logging.info(f"sendOnlinePaymentAsync: response={response}")


async def get_payment_details_async():
    async with grpc.aio.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = ecom_grpc_client.KodyEcomPaymentsServiceStub(channel)
        response = await stub.GetPayments(
            ecom_model.GetPaymentsRequest(store_id=config.store_id, page_cursor=PageCursor(page_size=1)),
            metadata=[("x-api-key", config.api_key)])

    logging.info(f"getPaymentDetailsAsync: response={response}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_online_payment_async())
    loop.run_until_complete(get_payment_details_async())
    loop.close()
