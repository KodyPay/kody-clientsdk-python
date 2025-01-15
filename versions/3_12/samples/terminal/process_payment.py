from datetime import datetime
import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

def send_terminal_payment():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your Terminal ID
    terminal_id = ""
    # TODO: Replace this with your API key
    api_key = ""
    # TODO: Replace this with your amount
    amount = "60"

    show_tips = True
    payment_method = kody_model.PaymentMethod(
        # Options: CARD, ALIPAY, WECHAT
        payment_method_type="CARD"
    )

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)
        response_iterator = client.Pay(
            kody_model.PayRequest(
                store_id=store_id,
                terminal_id=terminal_id,
                amount=amount,
                show_tips=show_tips,
                payment_method=payment_method
            ),
            metadata=[("x-api-key", api_key)]
        )

        for response in response_iterator:
            print(f"Order ID: {response.order_id}")
            if response.status:
                status = kody_model.PaymentStatus.Name(response.status)
                print(f"Status: {status}")
                print(f"Receipt JSON: {response.receipt_json}")
                print(f"Date Created: {datetime.fromtimestamp(response.date_created.seconds)}")
                print(f"Total Amount: {response.total_amount}")
                print(f"Sale Amount: {response.sale_amount}")
                print(f"Tips Amount: {response.tips_amount}")
                if status == "SUCCESS":
                    print(f"External Payment Reference: {response.ext_payment_ref}")
                elif status == "FAILED" or status == "CANCELLED":
                    print(f"Failure Reason: {response.failure_reason}")


if __name__ == "__main__":
    send_terminal_payment()