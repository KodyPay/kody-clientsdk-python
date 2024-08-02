import logging

import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as pay_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as pay_grpc_client

host = "grpc.kodypay.com:443"
storeId = "<YOUR_STORE_ID>"
key = "<YOUR_KEY>"


def run():
    with grpc.secure_channel(target=host,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = stub.Terminals(
            pay_model.TerminalsRequest(store_id=storeId),
            metadata=[("x-api-key", key)]
        )

    for i, terminal in enumerate(response.terminals):
        logging.info(f"Terminal {i}: id=[{terminal.terminal_id}], online=[{terminal.online}]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
