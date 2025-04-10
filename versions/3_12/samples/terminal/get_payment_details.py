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
            print(f"Receipt JSON: {payment_details_response.payment_data.receipt_json}")
            print(f"Date Created: {datetime.fromtimestamp(payment_details_response.date_created.seconds)}")
            print(f"Date Paid: {datetime.fromtimestamp(payment_details_response.payment_data.date_paid.seconds)}")
            print(f"Total Amount: {payment_details_response.payment_data.total_amount}")
            print(f"Sale Amount: {payment_details_response.payment_data.sale_amount}")
            print(f"Tips Amount: {payment_details_response.payment_data.tips_amount}")
            print(f"Payment method type: {kody_model.PaymentMethodType.Name(payment_details_response.payment_data.payment_method_type)}")
            print("Accepts only: " + ', '.join(kody_model.PayRequest.PaymentMethods.Name(paymentMethod) for paymentMethod in payment_details_response.accepts_only))
            if status == "SUCCESS":
                print(f"PSP Reference: {payment_details_response.psp_reference}")
            else:
                print(f"Failure Reason: {payment_details_response.failure_reason}")

if __name__ == "__main__":
    get_terminal_payment_details()