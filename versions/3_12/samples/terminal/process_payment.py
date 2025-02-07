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

    # Options: CARD, E-WALLET
    # Option 1: CARD
    payment_method = kody_model.PaymentMethod(
        payment_method_type=kody_model.PaymentMethodType.CARD,
    )

    # Options: VISA, MASTERCARD, AMEX, BAN_CONTACT, CHINA_UNION_PAY, MAESTRO, DINERS, DISCOVER, JCB, ALIPAY, WECHAT
    accepts_only = [
        kody_model.PayRequest.PaymentMethods.VISA,
        kody_model.PayRequest.PaymentMethods.MASTERCARD,
    ]

    # Option 2: E-WALLET
    # payment_method = kody_model.PaymentMethod(
    #     payment_method_type=kody_model.PaymentMethodType.E_WALLET,
    # )

    # # Options: VISA, MASTERCARD, AMEX, BAN_CONTACT, CHINA_UNION_PAY, MAESTRO, DINERS, DISCOVER, JCB, ALIPAY, WECHAT
    # # if you set E_WALLET, you have to at least add one of the following: ALIPAY, WECHAT
    # accepts_only = [
    #     kody_model.PayRequest.PaymentMethods.ALIPAY,
    #     kody_model.PayRequest.PaymentMethods.WECHAT,
    # ]

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
                print(f"Date Paid: {datetime.fromtimestamp(response.payment_data.date_paid.seconds)}")
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
