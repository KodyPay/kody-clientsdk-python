import grpc
import kody_clientsdk_python.pay.v1.pay_pb2 as kody_model
import kody_clientsdk_python.pay.v1.pay_pb2_grpc as kody_client

def get_terminals():
    # TODO: Replace this with the testing or live environment
    address = "grpc-staging.kodypay.com"
    # TODO: Replace this with your Store ID
    store_id = ""
    # TODO: Replace this with your API key
    api_key = ""

    with grpc.secure_channel(target=address,
                             credentials=grpc.ssl_channel_credentials()) as channel:
        client = kody_client.KodyPayTerminalServiceStub(channel)
        response = client.Terminals(
            kody_model.TerminalsRequest(store_id=store_id),
            metadata=[("x-api-key", api_key)]
        )

        for i, terminal in enumerate(response.terminals):
            print(f"Terminal {i}: id=[{terminal.terminal_id}], online=[{terminal.online}]")

if __name__ == "__main__":
    get_terminals()
