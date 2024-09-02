import configparser

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
    config_parser = configparser.SafeConfigParser()
    config_parser.read('config.ini')

    config = Config(address=config_parser.get("default", "address"),
                    store_id=config_parser.get("default", "storeId"),
                    api_key=config_parser.get("default", "apiKey"),
                    terminal_id=config_parser.get("default", "terminalId"))
    return config
