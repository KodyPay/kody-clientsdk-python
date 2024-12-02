import logging

import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

from ..config import load_config

config = load_config()


def send_terminal_payment() -> None:
    show_tips = True
    payment_method = kody_model.PaymentMethod(
        payment_method_type="CARD" # ALIPAY, WECHAT
    )

    # Big Decimal
    amount = "3.14"

    with grpc.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)
        response_iterator = client.Pay(
            kody_model.PayRequest(store_id=config.store_id, terminal_id=config.terminal_id, amount=amount,
                                  show_tips=show_tips, payment_method=payment_method),
            metadata=[("x-api-key", config.api_key)]
        )

        for response in response_iterator:
            logging.info(f"sendTerminalPayment: response={response}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    send_terminal_payment()
