import logging

import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as pay_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as pay_grpc_client

from ..config import load_config

config = load_config()


def get_terminals():
    with grpc.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = stub.Terminals(
            pay_model.TerminalsRequest(store_id=config.store_id),
            metadata=[("x-api-key", config.api_key)]
        )

        logging.info(f"getTerminals: response={response}")

        for i, terminal in enumerate(response.terminals):
            logging.info(f"Terminal {i}: id=[{terminal.terminal_id}], online=[{terminal.online}]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    get_terminals()
