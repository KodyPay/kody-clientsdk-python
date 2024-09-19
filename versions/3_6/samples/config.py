import os

class Config:
    def __init__(self, address, store_id, api_key, terminal_id, show_tips):
        self.address = address
        self.store_id = store_id
        self.api_key = api_key
        self.terminal_id = terminal_id
        self.show_tips = show_tips
        print(self)

    def __str__(self):
        return f'Config: address: {self.address}, store_id = {self.store_id,} api_key = {self.api_key}, terminal_id = {self.terminal_id}, show_tips = {self.show_tips}'

def load_config():

    config = Config(address=os.getenv('KODY_ADDRESS'),
                    store_id=os.getenv('KODY_STORE_ID'),
                    api_key=os.getenv('KODY_API_KEY'),
                    terminal_id=os.getenv('KODY_TERMINAL_ID'),
                    show_tips=os.getenv('SHOW_TIPS'))
    return config
