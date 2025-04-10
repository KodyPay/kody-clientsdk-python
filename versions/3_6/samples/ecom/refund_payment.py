import logging

import grpc
import kody_clientsdk_python.ecom.v1.ecom_pb2 as kody_model
import kody_clientsdk_python.ecom.v1.ecom_pb2_grpc as kody_client

from ..config import load_config

config = load_config()

def request_refund() -> None:
    #UUID
    payment_id = "" #Use an existing payment_id

    # Big Decimal
    amount = "" #Amount must be equal or less than the payment amount
    logging.info(
        f"requestRefund: store_id={config.store_id}, payment_id={payment_id}, amount={amount}")

    with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        kody_service = kody_client.KodyEcomPaymentsServiceStub(channel)
        response_iterator = kody_service.Refund(
            kody_model.RefundRequest(store_id=config.store_id, payment_id=payment_id,
                                     amount=amount),
            metadata=[("x-api-key", config.api_key)]
        )

        for response in response_iterator:
            logging.info(f"requestRefund: response={response}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    request_refund()
