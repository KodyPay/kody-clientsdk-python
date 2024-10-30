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
    config = Config(address='grpc-staging.kodypay.com',
                    # Set only the hostname and not the full url. Example: grpc.kodypay.com
                    store_id='4ac9ea63-9918-43d4-8da0-1dde11be29ab',
                    api_key='Du-SYvTdQEVST9ncVd6UHH7yD735h6iFi0IwoLscLlyD',
                    terminal_id='S1F2-000158240540290')
    return config
