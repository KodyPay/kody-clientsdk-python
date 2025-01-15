from datetime import datetime
import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

def get_terminal_payment_details():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your API key
    api_key = ""
    # TODO: Replace this with your order ID
    order_id = ""

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)

        payment_details_response = client.PaymentDetails(
            kody_model.PaymentDetailsRequest(store_id=store_id, order_id=order_id),
            metadata=[("x-api-key", api_key)]
        )

        print(f"Order ID: {payment_details_response.order_id}")
        if payment_details_response.status:
            status = kody_model.PaymentStatus.Name(payment_details_response.status)
            print(f"Status: {status}")
            print(f"Receipt JSON: {payment_details_response.receipt_json}")
            print(f"Total Amount: {payment_details_response.total_amount}")
            print(f"Date Created: {datetime.fromtimestamp(payment_details_response.date_created.seconds)}")
            print(f"Date Paid: {datetime.fromtimestamp(payment_details_response.date_paid.seconds)}")
            if status == "SUCCESS":
                print(f"External Payment Reference: {payment_details_response.ext_payment_ref}")
            else:
                print(f"Failure Reason: {payment_details_response.failure_reason}")

if __name__ == "__main__":
    get_terminal_payment_details()