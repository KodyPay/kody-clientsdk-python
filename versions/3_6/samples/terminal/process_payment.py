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
        # Options: CARD, E-WALLET
        payment_method_type="CARD"
    )

    # Options: VISA, MASTERCARD, AMEX, BAN_CONTACT, CHINA_UNION_PAY, MAESTRO, DINERS = 6, DISCOVER, JCB, ALIPAY, WECHAT
    accepts_only=["VISA", "MASTERCARD", "AMEX"]

    with grpc.secure_channel(target=address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)
        response_iterator = client.Pay(
            kody_model.PayRequest(
                store_id=store_id,
                terminal_id=terminal_id,
                amount=amount,
                show_tips=show_tips,
                payment_method=payment_method,
                accepts_only = accepts_only
            ),
            metadata=[("x-api-key", api_key)]
        )

        for response in response_iterator:
            print(f"Order ID: {response.idempotency_uuid}")
            if response.status:
                status = kody_model.PaymentStatus.Name(response.status)
                print(f"Status: {status}")
                print(f"Receipt JSON: {response.payment_data.receipt_json}")
                print(f"Date Created: {datetime.fromtimestamp(response.date_created.seconds)}")
                print(f"Total Amount: {response.payment_data.total_amount}")
                print(f"Sale Amount: {response.payment_data.sale_amount}")
                print(f"Tips Amount: {response.payment_data.tips_amount}")
                print(f"Payment method type: {kody_model.PaymentMethodType.Name(response.payment_data.payment_method_type)}")
                print("Accepts only: " + ', '.join(kody_model.PayRequest.PaymentMethods.Name(paymentMethod) for paymentMethod in response.accepts_only))

                if status == "SUCCESS":
                    print(f"PSP Reference: {response.psp_reference}")
                elif status == "FAILED" or status == "CANCELLED":
                    print(f"Failure Reason: {response.failure_reason}")


if __name__ == "__main__":
    send_terminal_payment()