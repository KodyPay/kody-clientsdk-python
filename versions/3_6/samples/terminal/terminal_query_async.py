import logging

import asyncio
import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as pay_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as pay_grpc_client

from samples.config import load_config

config = load_config()

async def get_terminals_async():
    async with grpc.aio.secure_channel(target=config.address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response = await stub.Terminals(
            pay_model.TerminalsRequest(store_id=config.store_id),
            metadata=[("x-api-key", config.api_key)]
        )

        logging.info(f"getTerminalsAsync: response={response}")

        for i, terminal in enumerate(response.terminals):
            logging.info(f"Terminal {i}: id=[{terminal.terminal_id}], online=[{terminal.online}]")


async def send_terminal_payment_async() -> None:
    #Big Decimal
    amount = "3.14"

    async with grpc.aio.secure_channel(target=config.address, credentials=grpc.ssl_channel_credentials()) as channel:
        stub = pay_grpc_client.KodyPayTerminalServiceStub(channel)
        response_iterator = stub.Pay(
            pay_model.PayRequest(store_id=config.store_id, terminal_id=config.terminal_id, amount=amount, show_tips=config.show_tips),
            metadata=[("x-api-key", config.api_key)]
        )

        async for response in response_iterator:
            logging.info(f"sendTerminalPaymentAsync: response={response}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Async code
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_terminals_async())
    loop.run_until_complete(send_terminal_payment_async())
    loop.close()
