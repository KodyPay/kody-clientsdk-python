import os


class Config:
    def __init__(self, address, store_id, api_key, terminal_id):
        self.address = address
        self.store_id = store_id
        self.api_key = api_key
        self.terminal_id = terminal_id
        print(self)

    def __str__(self):
        return f'Config: address: {self.address}, store_id = {self.store_id,} api_key = {self.api_key}, terminal_id = {self.terminal_id}'


def load_config():
    # load the configuration from the ENV variables
    # The address property must be only the hostname and not the full url.
    # Wrong: address='https://grpc.kodypay.com'
    # Correct: address='grpc.kodypay.com'
    config = Config(address=os.getenv('KODY_ADDRESS'),
                    store_id=os.getenv('KODY_STORE_ID'),
                    api_key=os.getenv('KODY_API_KEY'),
                    terminal_id=os.getenv('KODY_TERMINAL_ID'))
    return config
