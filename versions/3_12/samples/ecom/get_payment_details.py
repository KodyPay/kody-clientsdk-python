from datetime import datetime
import grpc

import kody_clientsdk_python.ecom.v1.ecom_pb2 as kody_model
import kody_clientsdk_python.ecom.v1.ecom_pb2_grpc as kody_client
from kody_clientsdk_python.sdk.common.pagination_pb2 import PageCursor

def get_payment_details():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your API key
    api_key = ""

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyEcomPaymentsServiceStub(channel)
        response = client.GetPayments(
            kody_model.GetPaymentsRequest(
                store_id=store_id,
                page_cursor=PageCursor(page_size=5)
            ),
            metadata=[("x-api-key", api_key)]
        )

    for payment in response.response.payments:
        print(f"Payment ID: {payment.payment_id}")
        print(f"Payment Reference: {payment.payment_reference}")
        print(f"Order ID: {payment.order_id}")
        print(f"Date Created: {datetime.fromtimestamp(payment.date_created.seconds)}")
        print(f"Status: {kody_model.PaymentDetailsResponse.Response.PaymentStatus.Name(payment.status)}")
        if payment.order_metadata != "":
            print(f"Order Metadata: {payment.order_metadata}")
        print("")


if __name__ == "__main__":
    get_payment_details()