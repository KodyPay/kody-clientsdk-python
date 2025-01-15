from datetime import datetime
import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

def request_refund():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your API key
    api_key = ""
    # TODO: Replace this with your order ID
    order_id = ""
    # TODO: Replace this with your amount
    amount = "1"

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)
        response_iterator = client.Refund(
            kody_model.RefundRequest(
                store_id=store_id,
                order_id=order_id,
                amount=amount
            ),
            metadata=[("x-api-key", api_key)]
        )

        for response in response_iterator:
            print(f"Order ID: {response.order_id}")
            if response.status:
                status = kody_model.RefundResponse.RefundStatus.Name(response.status)
                print(f"Status: {status}")
                print(f"Date Created: {datetime.fromtimestamp(response.date_created.seconds)}")
                print(f"Total Paid Amount: {response.total_paid_amount}")
                print(f"Total Amount Refunded: {response.total_amount_refunded}")
                print(f"Remaining Amount: {response.remaining_amount}")
                print(f"Total Amount Requested: {response.total_amount_requested}")
                print(f"Payment Transaction ID: {response.paymentTransactionId}")

if __name__ == "__main__":
    request_refund()